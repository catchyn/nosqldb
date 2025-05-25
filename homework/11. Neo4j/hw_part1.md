# NEO4J PRACTICE

## Несколько вариантов применения графовой базы данных

1. История съема квартир посуточно в приложении. Узлы это арендаторы, арендодатели и квартиры. Свойства узлов - рейтинг,
   возраст людей, местоположение квартиры. Свойства ребер - это сумма аренды, комментарий.
2. Интерактивная карта метро, поиск кратчайщего пути. Узлы станции метро и ребра это переходы между станциями.
3. Рекомендация музыки на основании того, что слушают люди с примерным совпадением по избранным трекам, либо прослушанным.
   Узлы это слушатели и песни. При совпадении на 75% можно попробовать посоветовать что-то из остальных 25% и т.п.

## Сравнение запросов в postgre и neo4j

- Создадим 3 таблицы: directors, movies, actors
- Создадим таблицы отношений: director_created_movie, actor_played_in_movie

```
CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER
);
CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE director_created_movie (
    director_id INTEGER REFERENCES directors(id),
    movie_id INTEGER REFERENCES movies(id),
    PRIMARY KEY (director_id, movie_id)
);
CREATE TABLE actor_played_in_movie (
    actor_id INTEGER REFERENCES actors(id),
    movie_id INTEGER REFERENCES movies(id),
    PRIMARY KEY (actor_id, movie_id)
);
```

### Создание нод и связей
```
#3 создание ноды
create (:Director {name:'Joel Coen'})
create (:Movie {title:'Blood Simple', year:1983})
#4 создание связи между существующими нодами, joel и blood - переменные
match (joel:Director {name:'Joel Coen'})
match (blood:Movie {title:'Blood Simple'})
create (joel) -[:CREATED]-> (blood)
#5 создание новой ноды и связи с существующей нодой
match (blood:Movie {title:'Blood Simple'})
create (:Actor {name: 'Frances McDormand'}) -[:PLAYED_IN]-> (blood)
```
```
-- 3
INSERT INTO directors (name) VALUES ('Joel Coen');
INSERT INTO movies (title, year) VALUES ('Blood Simple', 1983);
-- 4
INSERT INTO director_created_movie (director_id, movie_id)
VALUES (
    (SELECT id FROM directors WHERE name = 'Joel Coen'),
    (SELECT id FROM movies WHERE title = 'Blood Simple')
);
-- 5
INSERT INTO actors (name) VALUES ('Frances McDormand');
WITH actor_id AS (
    SELECT id FROM actors WHERE name = 'Frances McDormand'
),
movie_id AS (
    SELECT id FROM movies WHERE title = 'Blood Simple'
)
INSERT INTO actor_played_in_movie (actor_id, movie_id)
SELECT actor_id.id, movie_id.id
FROM actor_id, movie_id;
```

### Чтение

```
#17 найти ноду
match (joel:Director {name: 'Joel Coen'})
#18 найти ноду имеющую связь с другой нодой с указание метки Label нод
match (d:Director) -[r]- (m:Movie) return d, r, m
```
```
-- 17
SELECT * FROM directors
WHERE name = 'Joel Coen';
-- 18
SELECT d.id AS director_id,
       d.name AS director_name,
       'CREATED' AS relationship_type,
       m.id AS movie_id,
       m.title AS movie_title,
       m.year AS movie_year
FROM directors d
JOIN director_created_movie rel ON d.id = rel.director_id
JOIN movies m ON rel.movie_id = m.id;
```

### Обновление

```
#11 добавить свойство к ноде
match (n:Director {name:'Ethan Coen'})
SET n.born = 1957
#12 добавить свойство к связи
match (:Actor {name:'Frances McDormand'}) -[r:PLAYED_IN]-> (:Movie {title: 'Blood Simple'})
set r.character = 'Abby
```
```
-- 11
ALTER TABLE directors ADD COLUMN IF NOT EXISTS born INTEGER;
UPDATE directors
SET born = 1957
WHERE name = 'Ethan Coen';
-- 12
ALTER TABLE actor_played_in_movie ADD COLUMN IF NOT EXISTS character TEXT;
UPDATE actor_played_in_movie
SET character = 'Abby'
FROM actors a, movies m
WHERE
    actor_played_in_movie.actor_id = a.id
    AND actor_played_in_movie.movie_id = m.id
    AND a.name = 'Frances McDormand'
    AND m.title = 'Blood Simple';
```

### Удаление
```
#13 удалить ноду
match (martin:Director {name:'Martin Scorsese'}) delete martin
#16 удалить все ребра для ноды
match (n:Director {name:'Ethan Coen'}) -[r]- () delete r
```
```
-- 13
DELETE FROM directors
WHERE name = 'Martin Scorsese';
-- 16
DELETE FROM director_created_movie
WHERE director_id = (SELECT id FROM directors WHERE name = 'Ethan Coen');
```