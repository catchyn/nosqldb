# Tarantool practice

### Install

- Развернул докер `docker run --name mytarantool -p 3301:3301 -d tarantool/tarantool`

- Запустил console `docker exec -it mytarantool console`

### Task

1) Создаем space 'aviatickets' `box.schema.space.create('aviatickets')`
2) Формат space
```
box.space.aviatickets:format({
    {name='id',type='unsigned'},
    {name='airline',type='string'},
    {name='departure_date',type='unsigned'},
    {name='departure_city',type='string'},
    {name='arrival_city',type='string'},
    {name='min_price',type='double'},
})
```
3) Создаем индекс
```
box.space.aviatickets:create_index('ndx_primary',{parts={'id'}})
```
4) Создаем еще один индекс
```
box.space.aviatickets:create_index('ndx_secondary',{parts={'airline','departure_date','departure_city'}})
```
5) Создаем 10 записей
```
box.space.aviatickets:insert({1, 'Aeroflot', os.time{year=2025, month=1, day=1}, 'SVO', 'KUF', 4500.00})
box.space.aviatickets:insert({2, 'Pobeda', os.time{year=2025, month=1, day=5}, 'SVO', 'LED', 2500.00})
box.space.aviatickets:insert({3, 'Ural Airlines', os.time{year=2025, month=1, day=12}, 'LED', 'SVX', 5200.00})
box.space.aviatickets:insert({4, 'Smartavia', os.time{year=2025, month=1, day=7}, 'LED', 'MRV', 2900.00})
box.space.aviatickets:insert({5, 'S7 Airlines', os.time{year=2025, month=1, day=11}, 'DME', 'OVB', 6800.00})
box.space.aviatickets:insert({6, 'Red Wings', os.time{year=2025, month=1, day=1}, 'VKO', 'KRR', 2200.00})
box.space.aviatickets:insert({7, 'Nordwind', os.time{year=2025, month=1, day=14}, 'SVO', 'GOJ', 4200.00})
box.space.aviatickets:insert({8, 'Utair', os.time{year=2025, month=1, day=9}, 'ROV', 'AER', 2600.00})
box.space.aviatickets:insert({9, 'Rossiya', os.time{year=2025, month=1, day=1}, 'VKO', 'KGD', 3500.00})
box.space.aviatickets:insert({10, 'Pobeda', os.time{year=2025, month=1, day=6}, 'DME', 'KZN', 2700.00})
```
- Проверяем количество записей в space `box.space.aviatickets:count()` получаем число `10`
6) Ищем наименьшую стоимость:
- Создаем индекс для поиска по дате (использовать индекс `ndx_secondary` не вышло, а строить запрос полнотекстовый как будто бы неправильно)
`box.space.aviatickets:create_index('ndx_depdate', {parts={'departure_date'},unique=false})`
- Пишем функцию для поиска минимальной цены для указанной даты. 
```
function find_min_price()
    local target_date = os.time{year = 2025, month = 1, day = 1}
    local min_price = nil    
    for _, t in box.space.aviatickets.index.ndx_depdate:pairs(target_date) do
        if min_price == nil or t.min_price < min_price then
            min_price = t.min_price
        end
    end
    return min_price
end
```
- Вызываем `find_min_price()` ответ `2200`
7) Пишем функцию на Lua для вывода списка рейсов с минимальной стоимостью билета менее 3000 рублей
- Создаем индекс
`box.space.aviatickets:create_index('ndx_price', {parts = {'min_price'},unique = false})`
- пишем запрос
`box.space.aviatickets.index.idx_price:select({3000.00},{iterator = 'LT'})`
- получил результат
```
---                                                 
- - [4, 'Smartavia', 1736251200, 'LED', 'MRV', 2900]
  - [10, 'Pobeda', 1736164800, 'DME', 'KZN', 2700]  
  - [8, 'Utair', 1736424000, 'ROV', 'AER', 2600]    
  - [2, 'Pobeda', 1736078400, 'SVO', 'LED', 2500]   
  - [6, 'Red Wings', 1735732800, 'VKO', 'KRR', 2200]
...   
```