# Practice with clickhouse engines

### VersionedCollapsingMergeTree

```clickhouse
CREATE TABLE tbl1
(
    `UserID` UInt64,
    `PageViews` UInt8,
    `Duration` UInt8,
    `Sign` Int8,
    `Version` UInt8
)
    ENGINE = VersionedCollapsingMergeTree(Sign, Version)
    ORDER BY UserID

```
```clickhouse
INSERT INTO tbl1 VALUES (4324182021466249494, 5, 146, -1, 1);
INSERT INTO tbl1 VALUES (4324182021466249494, 5, 146, 1, 1),(4324182021466249494, 6, 185, 1, 2);
```
```clickhouse
SELECT * FROM tbl1;
```
```
   ┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
1. │ 4324182021466249494 │         5 │      146 │    1 │       1 │
2. │ 4324182021466249494 │         6 │      185 │    1 │       2 │
3. │ 4324182021466249494 │         5 │      146 │   -1 │       1 │
   └─────────────────────┴───────────┴──────────┴──────┴─────────┘
```
```clickhouse
SELECT * FROM tbl1 final;
```
```
   ┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
1. │ 4324182021466249494 │         6 │      185 │    1 │       2 │
   └─────────────────────┴───────────┴──────────┴──────┴─────────┘
```

Увидел поле version, понял что нужно использовать.

### SummingMergeTree

```clickhouse
CREATE TABLE tbl2
(
    key UInt32,
    value UInt32
)
ENGINE = SummingMergeTree
ORDER BY key;
```
```clickhouse
INSERT INTO tbl2 Values(1,1),(1,2),(2,1);
```
```clickhouse
select * from tbl2;
```
```
   ┌─key─┬─value─┐
1. │   1 │     3 │
2. │   2 │     1 │
   └─────┴───────┘
```

Видно что value просуммировалось, взял соответствующий движок.

### ReplacingMergeTree

```clickhouse
CREATE TABLE tbl3
(
`id` Int32,
`status` String,
`price` String,
`comment` String
)
ENGINE = ReplacingMergeTree
PRIMARY KEY (id)
ORDER BY (id, status);
```
```clickhouse
INSERT INTO tbl3 VALUES (23, 'success', '1000', 'Confirmed');
```
```clickhouse
INSERT INTO tbl3 VALUES (23, 'success', '2000', 'Cancelled');
```
```clickhouse
select * from tbl3
```
```
   ┌─id─┬─status──┬─price─┬─comment───┐
1. │ 23 │ success │ 1000  │ Confirmed │
2. │ 23 │ success │ 2000  │ Cancelled │
   └────┴─────────┴───────┴───────────┘
```
```clickhouse
select * from tbl3 final where id=23;
```
```
   ┌─id─┬─status──┬─price─┬─comment───┐
1. │ 23 │ success │ 2000  │ Cancelled │
   └────┴─────────┴───────┴───────────┘
```

Видно, что берется последнее значение из совпадений по условию, выбрал соотвветсвующий движок.

### AggregatingMergeTree

```clickhouse
CREATE TABLE tbl4
(
    `CounterID` UInt8,
    `StartDate` Date,
    `UserID` UInt64
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(StartDate)
ORDER BY (CounterID, StartDate)
```
```clickhouse
INSERT INTO tbl4 VALUES(0, '2019-11-11', 1);
```
```clickhouse
INSERT INTO tbl4 VALUES(1, '2019-11-12', 1);
```
```clickhouse
CREATE TABLE tbl5
(   CounterID UInt8,
    StartDate Date,
    UserID AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(StartDate) 
ORDER BY (CounterID, StartDate);
```
```clickhouse
INSERT INTO tbl5 SELECT
    CounterID,
    StartDate,
    uniqState(UserID)
FROM tbl4
GROUP BY
    CounterID,
    StartDate
```
```clickhouse
INSERT INTO tbl5 VALUES (1,'2019-11-12',1);
```
```
Code: 53. DB::Exception: Cannot convert UInt64 to AggregateFunction(uniq, UInt64): While executing 
ValuesBlockInputFormat: data for INSERT was parsed from query. (TYPE_MISMATCH) (version 25.3.2.39 (official build))
```
```clickhouse
SELECT uniqMerge(UserID) AS state
FROM tbl5
GROUP BY
    CounterID,
    StartDate
```
```
   ┌─state─┐
1. │     1 │
2. │     1 │
   └───────┘
```

Увидел что используетсся AggregateFunction, понятно какой engine использовать.

### CollapsingMergeTree

```clickhouse
CREATE TABLE tbl6
(
    `id` Int32,
    `status` String,
    `price` String,
    `comment` String,
    `sign` Int8
)
ENGINE = CollapsingMergeTree(sign)
PRIMARY KEY (id)
ORDER BY (id, status);
```
```clickhouse
INSERT INTO tbl6 VALUES (23, 'success', '1000', 'Confirmed', 1);
```
```clickhouse
INSERT INTO tbl6 VALUES (23, 'success', '1000', 'Confirmed', -1), (23, 'success', '2000', 'Cancelled', 1);
```
```clickhouse
SELECT * FROM tbl6;
```
```
   ┌─id─┬─status──┬─price─┬─comment───┬─sign─┐
1. │ 23 │ success │ 1000  │ Confirmed │   -1 │
2. │ 23 │ success │ 2000  │ Cancelled │    1 │
3. │ 23 │ success │ 1000  │ Confirmed │    1 │
   └────┴─────────┴───────┴───────────┴──────┘
```
```clickhouse
SELECT * FROM tbl6 FINAL;
```
```
   ┌─id─┬─status──┬─price─┬─comment───┬─sign─┐
1. │ 23 │ success │ 2000  │ Cancelled │    1 │
   └────┴─────────┴───────┴───────────┴──────┘
```

Реализовано обновление/отмена какой-то сущности через схлапывание.

### Проблемы

В данном ДЗ для tbl1 сначало использовал ReplaceMergeTree, но потом осозрнал, что нужно брать в расчет версию.
В 1 дз воевал с конфигами, почему то macros не хотел подтягиваться в конфиг.
Посмотрел 2 лекцию, осознал, что не дописал еще часть конфига и что можно было не править основной конфиг.
Забавно, что deepseek подсказывал реализовать описание конфига в yaml файликах, но в офф документации я такого не нашел.
