# CoachDB база

1. Посмотрел вебинар, ознакомился с приложенными документами.
2. Построил кластер из нод с CoachDB по аналогии с примером из практики.
```yaml
version: '3.9'
services:
  couchbase1:
    image: couchbase/server
    container_name: couchbase1
    volumes:
      - ./node1:/opt/couchbase/var
    ports:
      - 8094:8091
    networks:
      - db
  couchbase2:
    image: couchbase/server
    container_name: couchbase2
    volumes:
      - ./node2:/opt/couchbase/var
    ports:
      - 8095:8091
    networks:
      - db
  couchbase3:
    image: couchbase/server
    container_name: couchbase3
    volumes:
      - ./node3:/opt/couchbase/var
    ports:
      - 8091:8091
      - 8092:8092
      - 8093:8093
      - 11210:11210
    networks:
      - db
  couchbase4:
    image: couchbase/server
    container_name: couchbase4
    volumes:
      - ./node4:/opt/couchbase/var
    ports:
      - 8084:8091
    networks:
      - db
  couchbase5:
    image: couchbase/server
    container_name: couchbase5
    volumes:
      - ./node5:/opt/couchbase/var
    ports:
      - 8085:8091
    networks:
      - db
  couchbase6:
    image: couchbase/server
    container_name: couchbase6
    volumes:
      - ./node6:/opt/couchbase/var
    ports:
      - 8081:8091
    networks:
      - db

networks:
  db:
    # Specify driver options
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```
3. Настроил каждый инстанс на свои задачи, все инстансы работают в одной сети и видят друг друга.
4. Отключал по одному, при включении работа восстанавливается.
5. Добавил данные руками bucket -> scope -> collection -> document
6. Попытался сгенерить данные автоматически через nodejs и пакет nano. Столкнулся с ошибками 404, видимо какие то сетевые проблемы.
```js
const couch = require('nano')('http://admin:123456@localhost:8091');

const DB_NAME = 'films';

async function createFilms() {
    await couch.db.create(DB_NAME);
    const db = couch.db.use(DB_NAME);
    const testCoaches = [
        { _id: 'film_1', type: 'comedy', name: 'any', year: 1990 },
        { _id: 'film_2', type: 'horror', name: 'never', year: 2025 },
    ];

    await db.bulk({ docs: testCoaches });
}

createFilms();
```
