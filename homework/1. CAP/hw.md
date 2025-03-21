## MongoDB – CP/AP
MongoDB - это документоориентированная NoSQL DB. Позволяет настраивать уровни согласованности и доступности. Однако, она всегда стремится обеспечить устойчивость к разделению.
В случае сетевого разделения MongoDB допускает выбор нового первичного узла, чтобы продолжать работу. Используется вариация алгоритма RAFT, судя по документации.
Если консенсус не найден, то БД все равно будет работать на чтение тем самым останется доступной.

Для корректировки между Согласованностью(С) и Доступностью(A) используются настройки.
- [Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/) позволяет настраивать степень подтверждения записи.
По умолчанию, данные записываются в первичный узел, а репликация на вторичные узлы занимает время.  
- [Read Concern](http://mongodb.com/docs/manual/reference/read-concern/) позволяет настроить консистентность и изоляцию на чтение с точки зрения взаимодействия между нодами.
- [Read Preference](https://www.mongodb.com/docs/manual/core/read-preference/) позволяет настроить роутинг между клиентом и участником кластера. Идти в **PrimaryNode** или до **nearest** node и т.д.

По итогу, больше MongoDB склоняется в сторону CP, но может быть настроено и с уклоном в AP.

---

## MSSQL – CA
MSSQL – это реляционная DB, которая изначально не ориентирована на работу в распределенной среде, однако различными средствами эту работу поддерживает. Работает с транзакциями, а значит обеспечивает высокую согласованность данных.
Доступность также высокая, если нет проблем с сетью/железом.  

Устойчивость к разделению здесь отсутствует т.к. даже с учетом настроек кластера, если выбор новой PrimaryNode завершился неуспешно
(нет кворума), то кластер останавливает свою работу.

MSSQL соответствует CA.

---

## Cassandra – AP/CP
[Cassandra](http://cassandra.apache.org/_/cassandra-basics.html) – это NoSQL DB. Ее фишка хорошая масштабируемость и высокая доступность. 
Кластер представляет собой кольцо, а все ноды равноправны.
В кластере узлы для согласования используют **eventual consistency**, а значит эта БД пренебрегает консистентностью данных.
Однако данное поведение соответствует насройкам по-умолчанию. Если поковыряться в настройках, то можно улучшить консистентность, но в ущерб доступности.

Для взаимодействия между нодами используется **GOSSIP** алгоритм. Ноды выбирают N других узлов и шлют туда информацию о себе.
Целевые ноды передают информацию следующим N нодам и так далее. При разрыве сети каждый узел работает независимо и продолжает принимать запросы.
Репликация данных происходит асинхронно.