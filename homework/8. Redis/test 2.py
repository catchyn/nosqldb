import redis
import json
import time
import os
from collections import defaultdict

# Настройки
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
TEST_ITERATIONS = 5     # Количество итераций тестов
JSON_FILE = '20mb.json'  # Путь к JSON-файлу

# Инициализация клиента Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def load_json_data():
    """Загрузка данных из JSON-файла"""
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Преобразуем данные в словарь, если они в другом формате
    if isinstance(data, list):
        return {f"item_{i}": item for i, item in enumerate(data)}
    return data

def test_string(data):
    """Тест для хранения как строки"""
    # Запись
    start = time.time()
    r.set('test:string', json.dumps(data))
    write_time = time.time() - start

    # Чтение всего объекта
    start = time.time()
    result = json.loads(r.get('test:string'))
    read_time = time.time() - start

    # Чтение отдельных полей (имитация - требует полной десериализации)
    start = time.time()
    loaded_data = json.loads(r.get('test:string'))
    field_read_time = time.time() - start
    _ = [item.get('id', None) for item in loaded_data.values()]  # Пример чтения поля

    return {
        'write': write_time,
        'read': read_time,
        'field_read': field_read_time,
        'range_read': None,  # Не поддерживается для string
        'size': len(str(data))
    }

def test_hash(data):
    """Тест для хранения как хэша"""
    # Запись
    start = time.time()
    with r.pipeline() as pipe:
        for key, value in data.items():
            pipe.hset('test:hash', key, json.dumps(value))
        pipe.execute()
    write_time = time.time() - start

    # Чтение всего хэша
    start = time.time()
    result = {k: json.loads(v) for k, v in r.hgetall('test:hash').items()}
    read_time = time.time() - start

    # Чтение отдельных полей
    start = time.time()
    sample_key = next(iter(data.keys()))
    field_data = json.loads(r.hget('test:hash', sample_key))
    field_read_time = (time.time() - start) / len(data)  # Среднее время на поле

    # Диапазонные запросы (имитация - Redis HASH не поддерживает диапазоны)
    start = time.time()
    keys = r.hkeys('test:hash')[:10]  # Берем первые 10 ключей
    range_data = {k: json.loads(r.hget('test:hash', k)) for k in keys}
    range_read_time = time.time() - start

    return {
        'write': write_time,
        'read': read_time,
        'field_read': field_read_time,
        'range_read': None,  # Не поддерживается для string
        'size': None
    }

def test_zset(data):
    """Тест для sorted set"""
    # Запись
    start = time.time()
    with r.pipeline() as pipe:
        for key, value in data.items():
            # Используем первый числовой параметр как score
            score = float(next((v for v in value.values() if isinstance(v, (int, float))), 0))
            pipe.zadd('test:zset', {json.dumps(value): score})
        pipe.execute()
    write_time = time.time() - start

    # Чтение всего набора
    start = time.time()
    result = [json.loads(item) for item in r.zrange('test:zset', 0, -1)]
    read_time = time.time() - start

    # Чтение по диапазону scores
    start = time.time()
    min_score, max_score = 0, 100  # Пример диапазона
    range_result = [json.loads(item) for item in r.zrangebyscore('test:zset', min_score, max_score)]
    range_read_time = time.time() - start

    # Чтение отдельных элементов (имитация)
    start = time.time()
    first_item = json.loads(r.zrange('test:zset', 0, 0)[0])
    field_read_time = time.time() - start

    return {
        'write': write_time,
        'read': read_time,
        'field_read': None,
        'range_read': range_read_time,
        'size': None
    }

def test_list(data):
    """Тест для списка"""
    # Запись
    start = time.time()
    with r.pipeline() as pipe:
        for value in data.values():
            pipe.rpush('test:list', json.dumps(value))
        pipe.execute()
    write_time = time.time() - start

    # Чтение всего списка
    start = time.time()
    result = [json.loads(item) for item in r.lrange('test:list', 0, -1)]
    read_time = time.time() - start

    # Чтение по диапазону индексов
    start = time.time()
    range_result = [json.loads(item) for item in r.lrange('test:list', 0, 9)]  # Первые 10 элементов
    range_read_time = time.time() - start

    # Чтение отдельных элементов
    start = time.time()
    first_item = json.loads(r.lindex('test:list', 0))
    field_read_time = time.time() - start

    return {
        'write': write_time,
        'read': read_time,
        'field_read': field_read_time,
        'range_read': range_read_time,
        'size': None
    }

def run_tests():
    """Запуск всех тестов"""
    print(f"Загрузка данных из файла {JSON_FILE}...")
    try:
        test_data = load_json_data()
        data_size = len(test_data)
        print(f"Загружено {data_size} элементов")
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return

    print("\nЗапуск тестов...")
    results = defaultdict(list)

    for i in range(TEST_ITERATIONS):
        print(f"\nИтерация {i+1}/{TEST_ITERATIONS}")

        # Очистка предыдущих данных
        r.delete('test:string', 'test:hash', 'test:zset', 'test:list')

        # Запуск тестов
        results['string'].append(test_string(test_data))
        results['hash'].append(test_hash(test_data))
        results['zset'].append(test_zset(test_data))
        results['list'].append(test_list(test_data))

    # Анализ результатов
    print("\nРезультаты тестов (средние значения):")
    print(f"{'Тип':<8} {'Запись':<8} {'Чтение':<8} {'Чт.поля':<8} {'Диапазон':<8} {'Размер':<12}")
    print("-" * 60)

    for struct, tests in results.items():
        avg_write = sum(t['write'] for t in tests) / TEST_ITERATIONS
        avg_read = sum(t['read'] for t in tests) / TEST_ITERATIONS
        avg_field = sum(t['field_read'] or 0 for t in tests) / TEST_ITERATIONS
        avg_range = sum(t['range_read'] or 0 for t in tests) / TEST_ITERATIONS
        size_kb = (tests[0].get('size', 0) / 1024) if struct == 'string' else 'N/A'

        print(f"{struct.upper():<8} {avg_write:<8.4f} {avg_read:<8.4f} "
              f"{avg_field:<8.4f} {avg_range or '-':<8} {str(size_kb)[:7]:<12}")

if __name__ == "__main__":
    run_tests()