# NEO4J PRACTICE

### Взять 4-5 популярных туроператора.

- Coral Travel
- Anex Tour
- TEZ TOUR
- Библио-Глобус

### Каждый туроператор должен быть представлен в виде ноды neo4j 

```
create (:TourOperator {name:'Coral Travel'})
create (:TourOperator {name:'Anex Tour'})
create (:TourOperator {name:'TEZ TOUR'})
create (:TourOperator {name:'Библио-Глобус'})
```

### Взять 10-15 направлений, в которые данные операторы предосавляют путевки

### Представить направления в виде связки нод: страна - конкретное место

```
CREATE (russia:Country {name: "Россия"})-[:HAS_LOCATION]->(:Location {name: "Красная поляна"})
CREATE (russia)-[:HAS_LOCATION]->(:Location {name: "Кисловодск"})
CREATE (russia)-[:HAS_LOCATION]->(:Location {name: "Манжерок"})
CREATE (russia)-[:HAS_LOCATION]->(:Location {name: "Шерегеш"})
CREATE (:Country {name: "Армения"})-[:HAS_LOCATION]->(:Location {name: "Цакхадзор"})
CREATE (:Country {name: "Грузия"})-[:HAS_LOCATION]->(:Location {name: "Гудаури"})
CREATE (:Country {name: "Греция"})-[:HAS_LOCATION]->(:Location {name: "Санторини"})
CREATE (:Country {name: "Италия"})-[:HAS_LOCATION]->(:Location {name: "Рим"})
CREATE (:Country {name: "Франция"})-[:HAS_LOCATION]->(:Location {name: "Париж"})
CREATE (:Country {name: "ОАЭ"})-[:HAS_LOCATION]->(:Location {name: "Дубай"})
```

### Ближайшие города с аэропортами или вокзалами

```
MATCH (loc:Location {name: "Красная поляна"})
CREATE (:City {name: "Сочи", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Кисловодск"})
CREATE (:City {name: "Минеральные Воды", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Манжерок"})
CREATE (:City {name: "Горно-Алтайск", has_airport: false, has_train_station: false})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Шерегеш"})
CREATE (:City {name: "Новокузнецк", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Цакхадзор"})
CREATE (:City {name: "Ереван", has_airport: true, has_train_station: false})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Гудаури"})
CREATE (:City {name: "Тбилиси", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Санторини"})
CREATE (:City {name: "Афины", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Рим"})
CREATE (:City {name: "Рим", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Париж"})
CREATE (:City {name: "Париж", has_airport: true, has_train_station: true})-[:NEAR]->(loc)

MATCH (loc:Location {name: "Дубай"})
CREATE (:City {name: "Дубай", has_airport: true, has_train_station: false})-[:NEAR]->(loc)
```

### Создать связи между городами

Связи строю упрощая модель, пусть если есть вокзал или аэропорт можно лететь или ехать куда угодно,
если там есть соотвествующий транспортный объект.

```
MATCH (s:City {name: "Сочи"})
MATCH (m:City {name: "Минеральные Воды"})
MATCH (g:City {name: "Горно-Алтайск"})
MATCH (n:City {name: "Новокузнецк"})
MATCH (e:City {name: "Ереван"})
MATCH (t:City {name: "Тбилиси"})
MATCH (a:City {name: "Афины"})
MATCH (r:City {name: "Рим"})
MATCH (p:City {name: "Париж"})
MATCH (d:City {name: "Дубай"})

WITH {
    s: s,
    m: m,
    g: g,
    n: n,
    e: e,
    t: t,
    a: a,
    r: r,
    p: p,
    d: d
} AS cities

// Список всех пар городов и доступных видов транспорта между ними
UNWIND [
    {from: 's', to: 'm', transports: ['airplane', 'train']},
    {from: 's', to: 'g', transports: ['airplane']},
    {from: 's', to: 'n', transports: ['airplane', 'train']},
    {from: 's', to: 'e', transports: ['airplane']},
    {from: 's', to: 't', transports: ['airplane', 'train']},
    {from: 's', to: 'a', transports: ['airplane', 'train']},
    {from: 's', to: 'r', transports: ['airplane', 'train']},
    {from: 's', to: 'p', transports: ['airplane', 'train']},
    {from: 's', to: 'd', transports: ['airplane']},

    {from: 'm', to: 'g', transports: ['airplane']},
    {from: 'm', to: 'n', transports: ['airplane', 'train']},
    {from: 'm', to: 'e', transports: ['airplane']},
    {from: 'm', to: 't', transports: ['airplane', 'train']},
    {from: 'm', to: 'a', transports: ['airplane', 'train']},
    {from: 'm', to: 'r', transports: ['airplane', 'train']},
    {from: 'm', to: 'p', transports: ['airplane', 'train']},
    {from: 'm', to: 'd', transports: ['airplane']},

    {from: 'g', to: 'n', transports: ['airplane']},
    {from: 'g', to: 'e', transports: ['airplane']},
    {from: 'g', to: 't', transports: ['airplane']},
    {from: 'g', to: 'a', transports: ['airplane']},
    {from: 'g', to: 'r', transports: ['airplane']},
    {from: 'g', to: 'p', transports: ['airplane']},
    {from: 'g', to: 'd', transports: ['airplane']},

    {from: 'n', to: 'e', transports: ['airplane']},
    {from: 'n', to: 't', transports: ['airplane', 'train']},
    {from: 'n', to: 'a', transports: ['airplane', 'train']},
    {from: 'n', to: 'r', transports: ['airplane', 'train']},
    {from: 'n', to: 'p', transports: ['airplane', 'train']},
    {from: 'n', to: 'd', transports: ['airplane']},

    {from: 'e', to: 't', transports: ['airplane']},
    {from: 'e', to: 'a', transports: ['airplane']},
    {from: 'e', to: 'r', transports: ['airplane']},
    {from: 'e', to: 'p', transports: ['airplane']},
    {from: 'e', to: 'd', transports: ['airplane']},

    {from: 't', to: 'a', transports: ['airplane', 'train']},
    {from: 't', to: 'r', transports: ['airplane', 'train']},
    {from: 't', to: 'p', transports: ['airplane', 'train']},
    {from: 't', to: 'd', transports: ['airplane']},

    {from: 'a', to: 'r', transports: ['airplane', 'train']},
    {from: 'a', to: 'p', transports: ['airplane', 'train']},
    {from: 'a', to: 'd', transports: ['airplane']},

    {from: 'r', to: 'p', transports: ['airplane', 'train']},
    {from: 'r', to: 'd', transports: ['airplane']},

    {from: 'p', to: 'd', transports: ['airplane']}
] AS route

// Получаем узлы из мапы
WITH cities[route.from] AS fromCity, cities[route.to] AS toCity, route.transports AS transports

// Создаём маршруты в прямом направлении
FOREACH (transport IN transports |
    CREATE (fromCity)-[:ROUTE {transport: transport}]->(toCity)
)

// Создаём маршруты в обратном направлении
FOREACH (transport IN transports |
    CREATE (toCity)-[:ROUTE {transport: transport}]->(fromCity)
)
```

Получил граф как на рисунке [GRAPH](./graph.png)

### Написать запрос

Я не смог осознать, что значит "вывести направление который мог бы осуществить...".
Поэтому позволю себе немного подругому сформулировать: Получить все направления куда я могу добраться используя ЖД.
Предполагается, что все жд соединены в одну глобальную сеть.

```
MATCH ()-[r:ROUTE {transport: "train"}]->()-[:NEAR]->(l) return DISTINCT l
```

```
╒════════════════════════════════════╕
│l                                   │
╞════════════════════════════════════╡
│(:Location {name: "Красная поляна"})│
├────────────────────────────────────┤
│(:Location {name: "Кисловодск"})    │
├────────────────────────────────────┤
│(:Location {name: "Гудаури"})       │
├────────────────────────────────────┤
│(:Location {name: "Санторини"})     │
├────────────────────────────────────┤
│(:Location {name: "Рим"})           │
├────────────────────────────────────┤
│(:Location {name: "Париж"})         │
├────────────────────────────────────┤
│(:Location {name: "Шерегеш"})       │
└────────────────────────────────────┘
```

### Составить план запроса

```
EXPLAIN
MATCH ()-[r:ROUTE {transport: "train"}]->()-[:NEAR]->(l) return DISTINCT l
```

```
PROFILE
MATCH ()-[r:ROUTE {transport: "train"}]->()-[:NEAR]->(l) return DISTINCT l
```
Выполнение заняло 2ms

### Добавить индексы для оптимизации запроса

```
CREATE INDEX FOR ()-[r:ROUTE]-() ON (r.transport)
```

```
PROFILE
MATCH ()-[r:ROUTE {transport: "train"}]->()-[:NEAR]->(l) return DISTINCT l
```
Увидел, что индекс не используется, хотя был добавлен. Вероятно neo4j считает оптимизацию лишней для конкретно этого запроса.
