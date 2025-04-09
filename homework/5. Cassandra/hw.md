# Cassandra practice

1. Подготовил [docker-compose](./docker-compose.yaml) и поднял контейнеры. Создать кластер из 3х узлов.
2. Выполнил создание таблиц.
    - Создал keyspace `CREATE KEYSPACE my_keyspace
      WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};`
    - Создал tables:
      ```
      CREATE TABLE orders (
          country text,
          city text,
          order_id uuid,
          customer_name text,
          product_id uuid,
          total_amount decimal,
          PRIMARY KEY ((country, city), order_id)
      );
      ```
      ```
      CREATE TABLE products (
          id uuid PRIMARY KEY,
          name text,
          price decimal
      );
      ```         
      Partition key: country, city  
      Clustering key: order_id  
      Some other key: customer_name, total_amount...
3. Пролил данные используя [скрипт](./generate_data.sh)
4. Сделал несколько запросов к БД  

   - Простой запрос с Primary ключами
      ```cassandraql
      SELECT * FROM orders WHERE country='USA' AND city='New York';
      ```
      ```
       country | city     | order_id                             | customer_name | product_id                           | total_amount
      ---------+----------+--------------------------------------+---------------+--------------------------------------+--------------
           USA | New York | 08bf693c-5999-4271-a30a-6fc60aee1d5b |           Bob | cdc81965-a305-4a3a-b32d-52df1fe26a7a |      897.358
           USA | New York | 13442c6e-ac36-4241-b8ab-d505aa30d1f0 |           Eve | 593cea48-766d-42c5-9903-a6c66a4dc6b7 |      897.358
           USA | New York | 143ef7c7-894f-4ef9-93a9-0187ff0dd763 |           Bob | 383bf598-4e82-4e51-b95b-8bc612c059b6 |      1181.76
      ```
   - Запрос с кластерным ключем, в данном случае без какой либо пользы
     ```cassandraql
     SELECT * FROM orders WHERE country='USA' AND city='Boston' ORDER BY order_date DESC;
     ```
   - Запрос без индекса
     ```cassandraql
     SELECT * FROM products WHERE name='Product_55';
     ```
     Ответ
     ```
     InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
     ```
5. Создадим secondary индекс `CREATE INDEX product_name_idx ON products(name);` и повторим предыдущий запрос.  
     Ответ
     ```
     id                                   | name       | price
     --------------------------------------+------------+---------
     4854ae11-467f-4ebb-a16f-7a3ab416b488 | Product_55 | 231.935
     997258b2-214f-428d-a341-570280acfc65 | Product_55 | 161.137
     ```
6. Для стресс теста используется встроенный инструмент cassandra-stress.  
    Запустил 1кк операций с консистентностью на уровне ONE.
    ```shell
    /opt/cassandra/tools/bin/cassandra-stress write n=100000 cl=ONE -node cassandra-node1
    ```
    Результат
    ```
    Results:
    Op rate                   :   61,372 op/s  [WRITE: 61,372 op/s]
    Partition rate            :   61,372 pk/s  [WRITE: 61,372 pk/s]
    Row rate                  :   61,372 row/s [WRITE: 61,372 row/s]
    Latency mean              :    3.0 ms [WRITE: 3.0 ms]
    Latency median            :    1.6 ms [WRITE: 1.6 ms]
    Latency 95th percentile   :    9.3 ms [WRITE: 9.3 ms]
    Latency 99th percentile   :   21.5 ms [WRITE: 21.5 ms]
    Latency 99.9th percentile :   70.1 ms [WRITE: 70.1 ms]
    Latency max               :  446.4 ms [WRITE: 446.4 ms]
    Total partitions          :  1,000,000 [WRITE: 1,000,000]
    Total errors              :          0 [WRITE: 0]
    Total GC count            : 0
    Total GC memory           : 0.000 KiB
    Total GC time             :    0.0 seconds
    Avg GC time               :    NaN ms
    StdDev GC time            :    0.0 ms
    Total operation time      : 00:00:16
    ```