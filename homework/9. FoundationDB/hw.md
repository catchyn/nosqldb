# Разработать сервис для интернет-магазина

## Требования

### Usecases сервиса

- добавление товара
- загрузка товара по product_id
- изменение существующего товара
- удаление товара
- поиск товаров по диапазону цен
- поиск товаров по диапазону размеров

### Структура характеристик товара

```json
{
  "product_id": 180,
  "title": "Футболка",
  "price": 400.25,
  "size": 42
}
```

## Реализация

### Сервис

Написан сервис на Python и FastAPI.

Запуск:
```shell
docker-compose up --build
```

Команда для подключения к кластеру через cli:
```shell
docker exec -it fdb-coordinator fdbcli
```

swagger
```text
http://localhost:5000/docs
```

### Процесс

1) Добавлен товар из json в примере. Добавил через swagger, метод `/products/` и еще один придуманный json.
```shell
curl -X 'POST' \
  'http://localhost:5000/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": 181,
  "title": "Шорты",
  "price": 100,
  "size": 42
}'
```

В базе значение лежит как сериализованная строка:
`{"product_id": 180, "title": "\u0424\u0443\u0442\u0431\u043e\u043b\u043a\u0430", "price": 400.25, "size": 42}`

2) Получаю значение по идентификатору 180.
```shell
curl -X 'GET' \
  'http://localhost:5000/products/180' \
  -H 'accept: application/json'
```
Ответ:
```json
{
  "product_id": 180,
  "title": "Футболка",
  "price": 400.25,
  "size": 42
}
```

3) Изменение товара
```shell
curl -X 'PUT' \
  'http://localhost:5000/products/181' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "size": 52
}'
```

4) Удаление товара
```shell
curl -X 'DELETE' \
  'http://localhost:5000/products/181' \
  -H 'accept: application/json'
```

5) Поиск по диапазону цен
```shell
curl -X 'GET' \
  'http://localhost:5000/products/by_price/?min_price=0&max_price=1000' \
  -H 'accept: application/json'
```
```json
{
  "product_ids": [
    180,
    181
  ]
}
```

6) Поиск по диапазону размеров
```shell
curl -X 'GET' \
  'http://localhost:5000/products/by_size/?min_size=0&max_size=100' \
  -H 'accept: application/json'
```
```json
{
  "product_ids": [
    180,
    181
  ]
}
```