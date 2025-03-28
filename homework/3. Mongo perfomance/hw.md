# Практика с перфомансом шард/реплика БД на Mongo DB

## Подготовка

1. Составлен `docker-compose.yml` с нужными инстансами.
2. Запускаем командой `docker-compose -f ./docker-compose.yml up -d`
3. Инициируем кластеры.

конфиг сервер
```shell
rs.initiate({
  "_id" : "config-replica-set", 
  members : [
    {"_id" : 0, host : "mongo-configsvr-1:40001"},
    {"_id" : 1, host : "mongo-configsvr-2:40002"},
    {"_id" : 2, host : "mongo-configsvr-3:40003"}
  ]
});
```

шардинг 1 с 3 репликами
```shell
rs.initiate({
  "_id" : "shard-replica-set-1", 
  members : [
    {"_id" : 0, host : "mongo-shard-1-rs-1:40011"},
    {"_id" : 1, host : "mongo-shard-1-rs-2:40012"},
    {"_id" : 2, host : "mongo-shard-1-rs-3:40013"}
  ]
});
```

шардинг 2 с 3 репликами
```shell
rs.initiate({
  "_id" : "shard-replica-set-2", 
  members : [
    {"_id" : 0, host : "mongo-shard-2-rs-1:40021"},
    {"_id" : 1, host : "mongo-shard-2-rs-2:40022"},
    {"_id" : 2, host : "mongo-shard-2-rs-3:40023"}
  ]
});
```

шардинг 3 с 3 репликами
```shell
rs.initiate({
  "_id" : "shard-replica-set-3", 
  members : [
    {"_id" : 0, host : "mongo-shard-3-rs-1:40024"},
    {"_id" : 1, host : "mongo-shard-3-rs-2:40025"},
    {"_id" : 2, host : "mongo-shard-3-rs-3:40026"}
  ]
});
```

4. Добавил шарды
```shell
sh.addShard("shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013");
sh.addShard("shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023");
sh.addShard("shard-replica-set-3/mongo-shard-3-rs-1:40024,mongo-shard-3-rs-2:40025,mongo-shard-3-rs-3:40026"); 
```

5. sh.status()
```mongodb-json
...
shards
[
  {
    _id: 'shard-replica-set-1',
    host: 'shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013',
    state: 1,
    topologyTime: Timestamp({ t: 1743019322, i: 2 })
  },
  {
    _id: 'shard-replica-set-2',
    host: 'shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023',
    state: 1,
    topologyTime: Timestamp({ t: 1743019386, i: 2 })
  },
  {
    _id: 'shard-replica-set-3',
    host: 'shard-replica-set-3/mongo-shard-3-rs-1:40024,mongo-shard-3-rs-2:40025,mongo-shard-3-rs-3:40026',
    state: 1,
    topologyTime: Timestamp({ t: 1743019470, i: 2 })
  }
]
...
```

## Проливка данных

1. Чтобы не сочинять данные, для теста, воспользовался репозиторием из лекции про репликацию в mongo. Пролил 1кк записей через скрипт используя node.js.
2. DB у меня попала в shard-replica-set-3. В остальных шардах было пусто. Правило шардирования не было установлено, видимо поэтому mongos записи не раскидал.
3. Тест - проверим что будет, если я удалю db bank из mongos. Результат - ожидаемо db удалилась из shard-replica-set-3.
4. Дополнил коллекцию параметром 'artist' и 'sector' - случайное текстовое значение из списка значений и сгенерировал записи заново [script](insert-tickets.js).
5. DB попала уже в shard-replica-set-1, а значит mongos случайным образом выбирает, куда отправить данные.

## Индексы, правила шардирования

- Проверяем текущий статус коллекции `tickets`.
```
[direct: mongos] bank> db.tickets.getShardDistribution()
MongoshInvalidInputError: [SHAPI-10001] Collection tickets is not sharded
```
- Создадим индекс по полю 'sector'
`db.tickets.createIndex({sector: 1})`
- Создадим шард
`db.runCommand({shardCollection: "bank.tickets", key: {sector: 1}})`
- `sh.status()` показал разбиение на чанки, но видимо ключ не самый оптимальный т.к. один из шардов берет только 1 чанк.
```
collections: {
  'bank.tickets': {
    shardKey: { sector: 1 },
    unique: false,
    balancing: true,
    chunkMetadata: [
      { shard: 'shard-replica-set-1', nChunks: 1 },
      { shard: 'shard-replica-set-2', nChunks: 4 },
      { shard: 'shard-replica-set-3', nChunks: 4 }
    ],
    chunks: [
      { min: { sector: MinKey() }, max: { sector: 'C0R11' }, 'on shard': 'shard-replica-set-2', 'last modified': Timestamp({ t: 2, i: 0 }) },
      { min: { sector: 'C0R11' }, max: { sector: 'C0R14' }, 'on shard': 'shard-replica-set-3', 'last modified': Timestamp({ t: 3, i: 0 }) },
      { min: { sector: 'C0R14' }, max: { sector: 'C0R17' }, 'on shard': 'shard-replica-set-3', 'last modified': Timestamp({ t: 4, i: 0 }) },
      { min: { sector: 'C0R17' }, max: { sector: 'C0R2' }, 'on shard': 'shard-replica-set-2', 'last modified': Timestamp({ t: 5, i: 0 }) },
      { min: { sector: 'C0R2' }, max: { sector: 'C0R5' }, 'on shard': 'shard-replica-set-2', 'last modified': Timestamp({ t: 6, i: 0 }) },
      { min: { sector: 'C0R5' }, max: { sector: 'C0R8' }, 'on shard': 'shard-replica-set-3', 'last modified': Timestamp({ t: 7, i: 0 }) },
      { min: { sector: 'C0R8' }, max: { sector: 'C10R1' }, 'on shard': 'shard-replica-set-2', 'last modified': Timestamp({ t: 8, i: 0 }) },
      { min: { sector: 'C10R1' }, max: { sector: 'C10R12' }, 'on shard': 'shard-replica-set-3', 'last modified': Timestamp({ t: 9, i: 0 }) },
      { min: { sector: 'C10R12' }, max: { sector: MaxKey() }, 'on shard': 'shard-replica-set-1', 'last modified': Timestamp({ t: 9, i: 1 }) }
    ],
    tags: []
  }
}
```
- `db.tickets.getShardDistribution()` распределение по данным ровное, но один чанк получился монстром
```
Shard shard-replica-set-1 at shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013
{
  data: '35.98MiB',
  docs: 1000000,
  chunks: 1,
  'estimated data per chunk': '35.98MiB',
  'estimated docs per chunk': 1000000
}
---
Shard shard-replica-set-2 at shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023
{
  data: '34.13MiB',
  docs: 330000,
  chunks: 44,
  'estimated data per chunk': '794KiB',
  'estimated docs per chunk': 7500
}
---
Shard shard-replica-set-3 at shard-replica-set-3/mongo-shard-3-rs-1:40024,mongo-shard-3-rs-2:40025,mongo-shard-3-rs-3:40026
{
  data: '33.37MiB',
  docs: 322500,
  chunks: 43,
  'estimated data per chunk': '794KiB',
  'estimated docs per chunk': 7500
}
```

## Проверка выполнения при разных запросах

- `db.tickets.find({sector: 'C10R10'}).limit(5).explain("executionStats")`
Поиск происходил в одной реплике, но не учитывался индекс, хотя индекс был создан
- `db.tickets.find({amount: 44}).limit(20).explain("executionStats")`
Поиска происходил в разных шардаых `stage: 'SHARD_MERGE'` соответственно он менее эффективный
- развалил один из шардов полностью под ноль `db.tickets.getShardDistribution()`
`MongoServerError[FailedToSatisfyReadPreference]: Could not find host matching read preference { mode: "primary" } for set shard-replica-set-3`
Запросы выше также валятся с ошибкой, все пропало
- Поднял 2 ноды из 3х обратно, работоспособность восстановилась
- Уронил config-replica-set и попробовал добавить запись
`db.tickets.insertOne({name: 'turn', amount: 99, sector: 'C10R10', artist: 'KORN'})`
Получил ошибку
`MongoServerError: Write results unavailable from failing to target a host in the shard shard-replica-set-3 :: caused by :: Could not find host matching read preference { mode: "nearest" } for set config-replica-set`
- Поднял, работает штатно, запись прошла

## Авторизация

- Создал роль
`db.createRole({ role: "superRoot", privileges: [{ resource: { anyResource: true }, actions: ["anyAction"] }], roles: [] })`
- Создал админа, пользователя с правами на db bank
- включил аутентификацию и залогинился под пользователем, получаю ошибку при попытке админских действий
- залогинился под админом