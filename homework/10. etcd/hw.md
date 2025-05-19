# etcd practice

## Установка кластера

- Написал [docker-compose](./hw/docker-compose.yaml) и запустил `docker-compose up -d`
- Установил etcd manager
- Подключился, в настройках указал нужный ip адрес и порт. Увидел все 3 ноды etcd.

## Проверка работы кластера

- Установил ключ командой `docker exec -it etcd1 etcdctl put offer_key qwerty`
- Проверил, что реплика возвращает значение по ключу `docker exec -it etcd2 etcdctl get offer_key`.  
Вернулся и ключ и значение `offer_key`, `qwerty`.
- Выполнил команду `docker exec -it etcd1 etcdctl --write-out=table endpoint status ` увидел что etcd1 в данный момент лидер кластера.
- Останавливаю контейнер etcd1
- Выполняю `docker exec -it etcd2 etcdctl --write-out=table endpoint status` вижу, что прошел election и etcd2 теперь лидер
- Проверил, что etcd2 продолжает возвращать значение по ключу `docker exec -it etcd2 etcdctl get offer_key`.  
- Останавливаю контейнер etcd1. Кластер развалился, запросы на чтение падают с ошибкой `{"level":"warn","ts":"2025-05-19T21:45:44.591991Z","logger":"etcd-client","caller":"v3@v3.6.0/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc0002b34a0/127.0.
  0.1:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
  Error: context deadline exceeded`
- Поднял контейнеры etcd1 и etcd2, кластер ожил, значение возвращается

## Consul

- Поскольку consul аналогично реплицируется используя RAFT, результат проверки кластера будет схож.