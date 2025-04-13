# ClickHouse practice

## Развернуть БД

Создал файл [docker-compose.yaml](./docker-compose-single.yaml). Поднял контейнер.  
Подключился к контейнеру `docker exec -it 6clickhouse-clickhouse1-1 bash`
version 25.3.2.39

## Выполнить импорт тестовой БД

Импортировал БД trips из интрукции в [доке](https://clickhouse.com/docs/tutorial) clickhouse.

## Выполнить несколько запросов и оценить скорость выполнения

```clickhouse
-- Elapsed: 0.014 sec.
SELECT round(avg(tip_amount), 2)
FROM trips
```
```clickhouse
-- Elapsed: 0.015 sec.
SELECT max(trip_distance)
FROM trips
```
```clickhouse
-- Elapsed: 0.016 sec.
SELECT
    passenger_count,
    ceil(avg(total_amount), 2) AS average_total_amount
FROM trips
GROUP BY passenger_count
```
```clickhouse
-- 6 rows in set. Elapsed: 0.018 sec.
SELECT
    count(1) AS total,
    Borough
FROM trips
JOIN taxi_zone_dictionary ON toUInt64(trips.pickup_nyct2010_gid) = taxi_zone_dictionary.LocationID
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY Borough
ORDER BY total DESC
```

Работает быстро, 2 млн записей не чувствует при select и агрегациях.

# Развернуть БД из списка тестовых. Протестировать скорость запросов

У меня уже развернута база NYCTAXI, продолжу ее использовать но загружу не 2млн а 4млн записей.

```clickhouse
-- Средняя стоимость поездки по месяцам / 3 rows in set. Elapsed: 0.024 sec.
SELECT toMonth(pickup_date) AS month, avg(fare_amount) 
FROM trips 
GROUP BY month 
ORDER BY month;
```
```clickhouse
-- Поездки в Manhattan / 1 row in set. Elapsed: 0.065 sec.
SELECT count()
FROM trips
WHERE pickup_ntaname LIKE '%Manhattan%' 
   OR dropoff_ntaname LIKE '%Manhattan%';
```
```clickhouse
-- топ-10 самых дорогих поездок / 10 rows in set. Elapsed: 0.074 sec.
SELECT 
    trip_id,
    pickup_ntaname,
    dropoff_ntaname,
    trip_distance,
    total_amount
FROM trips
ORDER BY total_amount DESC
LIMIT 10;
```

# Развернуть Кликхаус в кластерном исполнении.

Поднял [докер](./docker-compose-cluster.yaml) с кластером clickHouse

Создать реляционную таблицу не получилось из-за проблем с конфигурацией кластера.
Нужно это решить на след. занятии.
