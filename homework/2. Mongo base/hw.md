# Практика с базовыми возможностями Mongo DB.

## Подготовка

- Установил mongo в docker на OS Windows
- Установил mongo tools и mongo compass
- Раскатил sample dataset из [github](https://github.com/neelabalan/mongodb-sample-dataset/blob/main/README.md) и подключился к базе

## Практика с методом Find

1. `db.movie.find()` вернул большой массив с фильмами, не поместился в shell
2. `db.comments.find({ movie_id: ObjectId('573a1391f29313caabcd70b4') })`  

```mongodb-json
{
_id: ObjectId('5a9427648b0beebeb6957ac8'),
name: 'Olenna Tyrell',
email: 'diana_rigg@gameofthron.es',
movie_id: ObjectId('573a1391f29313caabcd70b4'),
text: 'Sed iste tenetur ut. Veritatis deserunt iusto blanditiis similique reprehenderit. Expedita voluptas voluptatibus exercitationem odit. Saepe culpa dolorem error nulla.',
date: 2007-06-27T20:27:44.000Z
}
```

3. `db.movies.find({'awards.wins': 120});`
```mongodb-json
[{
  _id: ObjectId('573a139ef29313caabcfc5d8'),
  fullplot: "Lester and Carolyn Burnham are on the outside, a perfect husband and wife, in a perfect house, in a perfect neighborhood. But inside, Lester is slipping deeper and deeper into a hopeless depression. He finally snaps when he becomes infatuated with one of his daughter's friends. Meanwhile, his daughter Jane is developing a happy friendship with a shy boy-next-door named Ricky, who lives with an abusive father.",
  imdb: {
    rating: 8.4,
    votes: 741941,
    id: 169547
  },
  year: 1999,
  plot: "A sexually frustrated suburban father has a mid-life crisis after becoming infatuated with his daughter's best friend.",
  genres: [
    'Drama',
    'Romance'
  ],
  rated: 'R',
  metacritic: 86,
  title: 'American Beauty',
  lastupdated: '2015-08-31 00:00:30.340000000',
  languages: [
    'English'
  ],
  writers: [
    'Alan Ball'
  ],
  type: 'movie',
  tomatoes: {
    website: 'http://www.amazon.com/exec/obidos/subst/video/misc/dreamworks/american-beauty/ab-home.html/002-3821383-4244813',
    viewer: {
      rating: 3.8,
      numReviews: 656901,
      meter: 93
    },
    dvd: 2002-01-02T00:00:00.000Z,
    critic: {
      rating: 8.2,
      numReviews: 181,
      meter: 88
    },
    lastUpdated: 2015-09-12T17:05:27.000Z,
    consensus: "Flawlessly cast and brimming with dark, acid wit, American Beauty is a smart, provocative high point of late '90s mainstream Hollywood film.",
    rotten: 21,
    production: 'Dream Works',
    fresh: 160
  },
  poster: 'https://m.media-amazon.com/images/M/MV5BNTBmZWJkNjctNDhiNC00MGE2LWEwOTctZTk5OGVhMWMyNmVhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_SX677_AL_.jpg',
  num_mflix_comments: 388,
  released: 1999-10-01T00:00:00.000Z,
  awards: {
    wins: 120,
    nominations: 82,
    text: 'Won 5 Oscars. Another 115 wins & 82 nominations.'
  },
  countries: [
    'USA'
  ],
  cast: [
    'Kevin Spacey',
    'Annette Bening',
    'Thora Birch',
    'Wes Bentley'
  ],
  directors: [
    'Sam Mendes'
  ],
  runtime: 122
}]
```
4. `db.movies.find({'imdb.votes': {'$gt': 1500000}});`
```mongodb-json
[{
  _id: ObjectId('573a1399f29313caabceeb20'),
  fullplot: 'Andy Dufresne is a young and successful banker whose life changes drastically when he is convicted and sentenced to life imprisonment for the murder of his wife and her lover. Set in the 1940s, the film shows how Andy, with the help of his friend Red, the prison entrepreneur, turns out to be a most unconventional prisoner.',
  imdb: {
    rating: 9.3,
    votes: 1521105,
    id: 111161
  },
  year: 1994,
  plot: 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
  genres: [
    'Crime',
    'Drama'
  ],
  rated: 'R',
  metacritic: 80,
  title: 'The Shawshank Redemption',
  lastupdated: '2015-09-13 00:42:00.373000000',
  languages: [
    'English'
  ],
  writers: [
    'Stephen King (short story "Rita Hayworth and Shawshank Redemption")',
    'Frank Darabont (screenplay)'
  ],
  type: 'movie',
  tomatoes: {
    viewer: {
      rating: 4.4,
      numReviews: 878799,
      meter: 98
    },
    dvd: 1998-01-27T00:00:00.000Z,
    critic: {
      rating: 8.2,
      numReviews: 65,
      meter: 91
    },
    lastUpdated: 2015-09-10T17:30:15.000Z,
    consensus: 'The Shawshank Redemption is an uplifting, deeply satisfying prison drama with sensitive direction and fine performances.',
    rotten: 6,
    production: 'Columbia Pictures',
    fresh: 59
  },
  poster: 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_SX677_AL_.jpg',
  num_mflix_comments: 387,
  released: 1994-10-14T00:00:00.000Z,
  awards: {
    wins: 23,
    nominations: 16,
    text: 'Nominated for 7 Oscars. Another 16 wins & 16 nominations.'
  },
  countries: [
    'USA'
  ],
  cast: [
    'Tim Robbins',
    'Morgan Freeman',
    'Bob Gunton',
    'William Sadler'
  ],
  directors: [
    'Frank Darabont'
  ],
  runtime: 142
}]
```
5. `db.movies.find({year: {'$in': [2001, 2002]}}, { year: 1, title: 1, 'imdb.rating': 1}).limit(4);`
```mongodb-json
[{
  _id: ObjectId('573a1393f29313caabcdcb42'),
  title: 'Kate & Leopold',
  year: 2001,
  imdb: {
    rating: 6.3
  }
},
{
  _id: ObjectId('573a1398f29313caabceb1fe'),
  title: 'Crime and Punishment',
  year: 2002,
  imdb: {
    rating: 6.4
  }
},
{
  _id: ObjectId('573a139af29313caabcf0718'),
  imdb: {
    rating: 2.1
  },
  year: 2001,
  title: 'Glitter'
},
{
  _id: ObjectId('573a139af29313caabcf0718'),
  imdb: {
    rating: 2.1
  },
  year: 2001,
  title: 'Glitter'
}]
```
6. `db.movies.find({year: 2010, 'imdb.rating': {'$gte': 8.7}}, { year: 1, title: 1, 'imdb': 1, cast: 1})`
```mongodb-json
[{
  _id: ObjectId('573a13c5f29313caabd6ee61'),
  imdb: {
    rating: 8.8,
    votes: 1294646,
    id: 1375666
  },
  year: 2010,
  title: 'Inception',
  cast: [
    'Leonardo DiCaprio',
    'Joseph Gordon-Levitt',
    'Ellen Page',
    'Tom Hardy'
  ]
},
{
  _id: ObjectId('573a13c8f29313caabd78917'),
  cast: [
    'Heather Langenkamp',
    'Wes Craven',
    'Robert Englund',
    'Robert Shaye'
  ],
  title: 'Never Sleep Again: The Elm Street Legacy',
  year: 2010,
  imdb: {
    rating: 8.7,
    votes: 2610,
    id: 1510985
  }
}]
```
7. `db.movies.find({year: {'$in': [2007,2008,2009,2010]}, 'imdb.rating': {'$gte': 8.9}}, { year: 1, title: 1, 'imdb': 1, cast: 1}).sort({year: -1})`
```mongodb-json
[{
  _id: ObjectId('573a13c5f29313caabd6f5da'),
  cast: [
    'David Attenborough',
    'Joe Stevens'
  ],
  title: "Nature's Most Amazing Events",
  year: 2009,
  imdb: {
    rating: 9,
    votes: 2102,
    id: 1380596
  }
},{
  _id: ObjectId('573a13c9f29313caabd7a481'),
  cast: [
    'David Attenborough',
    'Oprah Winfrey'
  ],
  title: 'Life',
  year: 2009,
  imdb: {
    rating: 9.2,
    votes: 16807,
    id: 1533395
  }
},{
  _id: ObjectId('573a13b5f29313caabd42722'),
  imdb: {
    rating: 9,
    votes: 1495351,
    id: 468569
  },
  year: 2008,
  title: 'The Dark Knight',
  cast: [
    'Christian Bale',
    'Heath Ledger',
    'Aaron Eckhart',
    'Michael Caine'
  ]
},{
  _id: ObjectId('573a13b5f29313caabd42722'),
  imdb: {
    rating: 9,
    votes: 1495351,
    id: 468569
  },
  year: 2008,
  title: 'The Dark Knight',
  cast: [
    'Christian Bale',
    'Heath Ledger',
    'Aaron Eckhart',
    'Michael Caine'
  ]
}]
```
8. `db.movies.find({year: {'$in': [2007,2008,2009,2010]}, 'imdb.rating': {'$gte': 8.9}}, { year: 1, title: 1, 'imdb': 1, cast: 1}).sort({year: -1}).limit(1)`
```mongodb-json
{
  _id: ObjectId('573a13c5f29313caabd6f5da'),
  cast: [
    'David Attenborough',
    'Joe Stevens'
  ],
  title: "Nature's Most Amazing Events",
  year: 2009,
  imdb: {
    rating: 9,
    votes: 2102,
    id: 1380596
  }
}
```
9. `db.movies.find({year: {'$in': [2007,2008,2009,2010]}, 'imdb.rating': {'$gte': 8.9}}, { year: 1, title: 1, cast: 1}).sort({year: -1}).skip(2)`
```mongodb-json
[{
  _id: ObjectId('573a13b5f29313caabd42722'),
  year: 2008,
  title: 'The Dark Knight',
  cast: [
    'Christian Bale',
    'Heath Ledger',
    'Aaron Eckhart',
    'Michael Caine'
  ]
},{
  _id: ObjectId('573a13bdf29313caabd5867a'),
  cast: [
    'Keith David',
    'Katharine Phillips',
    'Tom Hanks',
    'Paul Fussell'
  ],
  title: 'The War',
  year: 2007
}]
```
10. `db.movies.find({ $and: [{year: 2000}, {'imdb.rating': {$gte: 7.5}}] }, {title: 1, year: 1, 'imdb.rating': 1}).limit(1)`
```mongodb-json
{
  _id: ObjectId('573a139af29313caabcf0782'),
  imdb: {
    rating: 8.1
  },
  year: 2000,
  title: 'In the Mood for Love'
}
```
`db.movies.find({poster: {$exists: true}}, {poster: 1}).limit(2)`
```mongodb-json
[{
  _id: ObjectId('573a1390f29313caabcd42e8'),
  poster: 'https://m.media-amazon.com/images/M/MV5BMTU3NjE5NzYtYTYyNS00MDVmLWIwYjgtMmYwYWIxZDYyNzU2XkEyXkFqcGdeQXVyNzQzNzQxNzI@._V1_SY1000_SX677_AL_.jpg'
},{
  _id: ObjectId('573a1390f29313caabcd5c0f'),
  poster: 'https://m.media-amazon.com/images/M/MV5BZTc0YjA1ZjctOTFlZi00NWRiLWE2MTAtZDE1MWY1YTgzOTJjXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SY1000_SX677_AL_.jpg'
}]
```

## Практика Insert

1. Добавим один комментарий к фильму ObjectId('573a13bdf29313caabd5867a').

`db.comments.insertOne({name: 'Alex Li', email: 'somebody@gmail.com', movie_id: ObjectId('573a13bdf29313caabd5867a'), text: 'Nice movie!',date: new Date()})`
```mongodb-json
{
  acknowledged: true,
  insertedId: ObjectId('67d8f11c240b5be7bb777a46')
}
```
`db.comments.find({movie_id: ObjectId('573a13bdf29313caabd5867a'), name: 'Alex Li'})`
```mongodb-json
{
  _id: ObjectId('67d8f11c240b5be7bb777a46'),
  name: 'Alex Li',
  email: 'somebody@gmail.com',
  movie_id: ObjectId('573a13bdf29313caabd5867a'),
  text: 'Nice movie!',
  date: 2025-03-18T04:05:48.907Z
}
```

2. Добавим еще несколько комментариев.
```
db.comments.insertMany([
{
    name: 'Alex',
    email: 'somebody@gmail.com',
    movie_id: ObjectId('573a13bdf29313caabd5867a'),
    text: 'Bad movie!',
    date: new Date()
}, {
    name: 'Peter',
    email: 'somepeter@gmail.com',
    movie_id: ObjectId('573a13bdf29313caabd5867a'),
    text: 'Horror movie!',
    date: new Date()
}])
```
```mongodb-json
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('67d8f377240b5be7bb777a47'),
    '1': ObjectId('67d8f377240b5be7bb777a48')
  }
}
```

`db.comments.find({movie_id: ObjectId('573a13bdf29313caabd5867a'), date: {$gte: new Date('2025-03-18T04:00:00Z')}})`
```mongodb-json
[{
  _id: ObjectId('67d8f11c240b5be7bb777a46'),
  name: 'Alex Li',
  email: 'somebody@gmail.com',
  movie_id: ObjectId('573a13bdf29313caabd5867a'),
  text: 'Nice movie!',
  date: 2025-03-18T04:05:48.907Z
},{
  _id: ObjectId('67d8f377240b5be7bb777a47'),
  name: 'Alex',
  email: 'somebody@gmail.com',
  movie_id: ObjectId('573a13bdf29313caabd5867a'),
  text: 'Bad movie!',
  date: 2025-03-18T04:15:51.748Z
},{
  _id: ObjectId('67d8f377240b5be7bb777a47'),
  name: 'Alex',
  email: 'somebody@gmail.com',
  movie_id: ObjectId('573a13bdf29313caabd5867a'),
  text: 'Bad movie!',
  date: 2025-03-18T04:15:51.748Z
}]
```

## Практика Update

1. Изменим имя в комментарии

`db.comments.updateOne({name: 'Alex Li'}, {$set: {name: 'Alex'}})`
```mongodb-json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
```
`db.comments.find({movie_id: ObjectId('573a13bdf29313caabd5867a'), date: {$gte: new Date('2025-03-18T04:00:00Z')}})`

2. Изменим email

`db.comments.updateMany({name: 'Alex'},{$set: {email: 'somealex@gmail.com'}})`
```mongodb-json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 2,
  modifiedCount: 2,
  upsertedCount: 0
}
```

`db.comments.find({movie_id: ObjectId('573a13bdf29313caabd5867a'), date: {$gte: new Date('2025-03-18T04:00:00Z')}},{name: 1, email: 1})`
```mongodb-json
[{
  _id: ObjectId('67d8f11c240b5be7bb777a46'),
  name: 'Alex',
  email: 'somealex@gmail.com'
},{
  _id: ObjectId('67d8f377240b5be7bb777a47'),
  name: 'Alex',
  email: 'somealex@gmail.com'
},{
  _id: ObjectId('67d8f377240b5be7bb777a48'),
  name: 'Peter',
  email: 'somepeter@gmail.com'
}]
```

## Задание на создание индекса и сравнение до/после

- Осознал, что у меня 4 версия mongo, сломался Mongo compass. Поставил последнюю версию mongo community жизнь наладилась.
- оптимизируем запрос `db.movies.find({year: {'$in': [2007,2008,2009,2010]}, 'imdb.rating': {'$gte': 8.9}}, { year: 1, title: 1, cast: 1}).sort({year: -1})`
- измерим время выполнения `db.movies.find({year: {'$in': [2007,2008,2009,2010]}, 'imdb.rating': {'$gte': 8.9}}, { year: 1, title: 1, cast: 1}).sort({year: -1}).explain("executionStats")`
```mongodb-json
{
  explainVersion: '1',
  queryPlanner: {
    namespace: 'sample_mflix.movies',
    indexFilterSet: false,
    parsedQuery: {
      '$and': [
        { 'imdb.rating': { '$gte': 8.9 } },
        { year: { '$in': [ 2007, 2008, 2009, 2010 ] } }
      ]
    },
    queryHash: 'AEAB29D6',
    planCacheKey: 'AEAB29D6',
    maxIndexedOrSolutionsReached: false,
    maxIndexedAndSolutionsReached: false,
    maxScansToExplodeReached: false,
    winningPlan: {
      stage: 'SORT',
      sortPattern: { year: -1 },
      memLimit: 104857600,
      type: 'simple',
      inputStage: {
        stage: 'PROJECTION_SIMPLE',
        transformBy: { year: 1, title: 1, cast: 1 },
        inputStage: {
          stage: 'COLLSCAN',
          filter: {
            '$and': [
              { 'imdb.rating': { '$gte': 8.9 } },
              { year: { '$in': [ 2007, 2008, 2009, 2010 ] } }
            ]
          },
          direction: 'forward'
        }
      }
    },
    rejectedPlans: []
  },
  executionStats: {
    executionSuccess: true,
    nReturned: 4,
    executionTimeMillis: 12,
    totalKeysExamined: 0,
    totalDocsExamined: 23539,
    executionStages: {
      stage: 'SORT',
      nReturned: 4,
      executionTimeMillisEstimate: 0,
      works: 23545,
      advanced: 4,
      needTime: 23540,
      needYield: 0,
      saveState: 23,
      restoreState: 23,
      isEOF: 1,
      sortPattern: { year: -1 },
      memLimit: 104857600,
      type: 'simple',
      totalDataSizeSorted: 660,
      usedDisk: false,
      spills: 0,
      spilledDataStorageSize: 0,
      inputStage: {
        stage: 'PROJECTION_SIMPLE',
        nReturned: 4,
        executionTimeMillisEstimate: 0,
        works: 23540,
        advanced: 4,
        needTime: 23535,
        needYield: 0,
        saveState: 23,
        restoreState: 23,
        isEOF: 1,
        transformBy: { year: 1, title: 1, cast: 1 },
        inputStage: {
          stage: 'COLLSCAN',
          filter: {
            '$and': [
              { 'imdb.rating': { '$gte': 8.9 } },
              { year: { '$in': [ 2007, 2008, 2009, 2010 ] } }
            ]
          },
          nReturned: 4,
          executionTimeMillisEstimate: 0,
          works: 23540,
          advanced: 4,
          needTime: 23535,
          needYield: 0,
          saveState: 23,
          restoreState: 23,
          isEOF: 1,
          direction: 'forward',
          docsExamined: 23539
        }
      }
    }
  command: {
    find: 'movies',
    filter: {
      year: { '$in': [ 2007, 2008, 2009, 2010 ] },
      'imdb.rating': { '$gte': 8.9 }
    },
    sort: { year: -1 },
    projection: { year: 1, title: 1, cast: 1 },
    '$db': 'sample_mflix'
  },
  serverInfo: {
    host: 'a89e64f73628',
    port: 27017,
    version: '7.0.17',
    gitVersion: 'f099987179b0e9919aa2fcba25afe48f35e53ae9'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'forceClassicEngine'
  },
  ok: 1
}
```
- нашел `executionTimeMillis: 12`, 12ms время выполнения запроса
- проверяем текущие индексы `db.movies.getIndexes()`. Есть индекс по _id.
```mongodb-json
[ { v: 2, key: { _id: 1 }, name: '_id_' } ]
```
- создаю индекс `db.movies.createIndex("year": 1, 'imdb.rating': 1)`
Возвращается имя нового индекса `year_1_imdb.rating_1`
- повторяю запрос `db.movies.find({year: {'$in': [2007,2008,2009,2010]}, 'imdb.rating': {'$gte': 8.9}}, { year: 1, title: 1, cast: 1}).sort({year: -1}).explain("executionStats")`
```mongodb-json
{
  explainVersion: '1',
  queryPlanner: {
    namespace: 'sample_mflix.movies',
    indexFilterSet: false,
    parsedQuery: {
      '$and': [
        { 'imdb.rating': { '$gte': 8.9 } },
        { year: { '$in': [ 2007, 2008, 2009, 2010 ] } }
      ]
    },
    queryHash: 'AEAB29D6',
    planCacheKey: '69FE6204',
    maxIndexedOrSolutionsReached: false,
    maxIndexedAndSolutionsReached: false,
    maxScansToExplodeReached: false,
    winningPlan: {
      stage: 'PROJECTION_SIMPLE',
      transformBy: { year: 1, title: 1, cast: 1 },
      inputStage: {
        stage: 'FETCH',
        inputStage: {
          stage: 'IXSCAN',
          keyPattern: { year: 1, 'imdb.rating': 1 },
          indexName: 'year_1_imdb.rating_1',
          isMultiKey: false,
          multiKeyPaths: { year: [], 'imdb.rating': [] },
          isUnique: false,
          isSparse: false,
          isPartial: false,
          indexVersion: 2,
          direction: 'backward',
          indexBounds: {
            year: [
              '[2010, 2010]',
              '[2009, 2009]',
              '[2008, 2008]',
              '[2007, 2007]'
            ],
            'imdb.rating': [ '[inf.0, 8.9]' ]
          }
        }
      }
    },
    rejectedPlans: []
  },
  executionStats: {
    executionSuccess: true,
    nReturned: 4,
    executionTimeMillis: 1,
    totalKeysExamined: 9,
    totalDocsExamined: 4,
    executionStages: {
      stage: 'PROJECTION_SIMPLE',
      nReturned: 4,
      executionTimeMillisEstimate: 0,
      works: 9,
      advanced: 4,
      needTime: 4,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      transformBy: { year: 1, title: 1, cast: 1 },
      inputStage: {
        stage: 'FETCH',
        nReturned: 4,
        executionTimeMillisEstimate: 0,
        works: 9,
        advanced: 4,
        needTime: 4,
        needYield: 0,
        saveState: 0,
        restoreState: 0,
        isEOF: 1,
        docsExamined: 4,
        alreadyHasObj: 0,
        inputStage: {
          stage: 'IXSCAN',
          nReturned: 4,
          executionTimeMillisEstimate: 0,
          works: 9,
          advanced: 4,
          needTime: 4,
          needYield: 0,
          saveState: 0,
          restoreState: 0,
          isEOF: 1,
          keyPattern: { year: 1, 'imdb.rating': 1 },
          indexName: 'year_1_imdb.rating_1',
          isMultiKey: false,
          multiKeyPaths: { year: [], 'imdb.rating': [] },
          isUnique: false,
          isSparse: false,
          isPartial: false,
          indexVersion: 2,
          direction: 'backward',
          indexBounds: {
            year: [
              '[2010, 2010]',
              '[2009, 2009]',
              '[2008, 2008]',
              '[2007, 2007]'
            ],
            'imdb.rating': [ '[inf.0, 8.9]' ]
          },
          keysExamined: 9,
          seeks: 5,
          dupsTested: 0,
          dupsDropped: 0
        }
      }
  },
  command: {
    find: 'movies',
    filter: {
      year: { '$in': [ 2007, 2008, 2009, 2010 ] },
      'imdb.rating': { '$gte': 8.9 }
    },
    sort: { year: -1 },
    projection: { year: 1, title: 1, cast: 1 },
    '$db': 'sample_mflix'
  },
  serverInfo: {
    host: 'a89e64f73628',
    port: 27017,
    version: '7.0.17',
    gitVersion: 'f099987179b0e9919aa2fcba25afe48f35e53ae9'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'forceClassicEngine'
  },
  ok: 1
}
```
- видим, что `executionTimeMillis: 1` 1ms, блок winningPlan включает stage 'IXSCAN' и name ранее созданного индекса. Успех. 