# KAFKA PRACTICE

### INSTALL KAFKA

- Разворачиваем docker container `docker compose up -d`

### Базовое использование KAFKA через бинарники, задание 1-3

- создаем топик `test-topic` командой `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic`
- публикуем сообщения в брокер через producer `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic`
- Вводим тестовые сообщения `>message1`, `>message2`
- Подключаем consumer `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning`
- Видим что сообщения получены


```
I have no name!@59647895d586:/$ kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic
Created topic test-topic.
I have no name!@59647895d586:/$ kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
>message1
>message2
>^CI have no name!@59647895d586:/$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning
message1
message2
```

### Использование KAFKA с сервисом на nodejs

- Собираем скрипт с kafkajs `docker-compose build --no-cache`
- Запускаем compose `docker-compose up -d`
- Смотрим лог по сервису `docker-compose logs node-app` видно по логам,
что сообщения отправились в топик `any-message-topic` и что consumer 
получил сообщения:
```
node-app-1  | new message from consumer--topic:any-message-topic--partition:0--value:Test message from nodejs app--fullMessage:{"magicByte":2,"attributes":0,"timestamp":"1750159576824","offset":"0","key":nu
ll,"value":{"type":"Buffer","data":[84,101,115,116,32,109,101,115,115,97,103,101,32,102,114,111,109,32,110,111,100,101,106,115,32,97,112,112]},"headers":{},"isControlRecord":false,"batchContext":{"firstOffs
et":"0","firstTimestamp":"1750159576824","partitionLeaderEpoch":0,"inTransaction":false,"isControlBatch":false,"lastOffsetDelta":1,"producerId":"-1","producerEpoch":0,"firstSequence":0,"maxTimestamp":"17501
59576824","timestampType":0,"magicByte":2}}
node-app-1  | new message from consumer--topic:any-message-topic--partition:0--value:Another test message from nodejs app--fullMessage:{"magicByte":2,"attributes":0,"timestamp":"1750159576824","offset":"1",
"key":null,"value":{"type":"Buffer","data":[65,110,111,116,104,101,114,32,116,101,115,116,32,109,101,115,115,97,103,101,32,102,114,111,109,32,110,111,100,101,106,115,32,97,112,112]},"headers":{},"isControlR
ecord":false,"batchContext":{"firstOffset":"0","firstTimestamp":"1750159576824","partitionLeaderEpoch":0,"inTransaction":false,"isControlBatch":false,"lastOffsetDelta":1,"producerId":"-1","producerEpoch":0,
"firstSequence":0,"maxTimestamp":"1750159576824","timestampType":0,"magicByte":2}}
```