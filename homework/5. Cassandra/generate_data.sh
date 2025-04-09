#!/bin/bash

KEYSPACE="my_keyspace"
PRODUCT_FILE="products.txt"
ORDER_FILE="orders.cql"
PRODUCT_COUNT=1000
ORDER_COUNT=1000

echo "Generating $PRODUCT_COUNT products..."
echo "USE $KEYSPACE;" > insert_products.cql
> $PRODUCT_FILE

for i in $(seq 1 $PRODUCT_COUNT); do
  uuid=$(uuidgen)
  name="Product_$i"
  price=$(awk -v min=10 -v max=1000 'BEGIN{srand(); print min+rand()*(max-min)}')
  echo "$uuid" >> $PRODUCT_FILE
  echo "INSERT INTO products (id, name, price) VALUES ($uuid, '$name', $price);" >> insert_products.cql
done

echo "Inserting products into Cassandra..."
cqlsh < insert_products.cql

echo "Generating $ORDER_COUNT orders..."
> $ORDER_FILE
echo "USE $KEYSPACE;" > $ORDER_FILE

cities=("New York" "Boston" "Los Angeles" "Chicago" "Seattle")
countries=("USA" "Canada" "UK" "Germany" "France")
customers=("Alice" "Bob" "Charlie" "Diana" "Eve")

for i in $(seq 1 $ORDER_COUNT); do
  uuid=$(uuidgen)
  country=${countries[$RANDOM % ${#countries[@]}]}
  city=${cities[$RANDOM % ${#cities[@]}]}
  customer=${customers[$RANDOM % ${#customers[@]}]}
  product_id=$(shuf -n 1 $PRODUCT_FILE)
  amount=$(awk -v min=5 -v max=2000 'BEGIN{srand(); print min+rand()*(max-min)}')

  echo "INSERT INTO orders (country, city, order_id, customer_name, product_id, total_amount)
        VALUES ('$country', '$city', $uuid, '$customer', $product_id, $amount);" >> $ORDER_FILE
done

echo "Inserting orders into Cassandra (may take a while)..."
cqlsh < $ORDER_FILE

echo "✅ Done inserting $PRODUCT_COUNT products and $ORDER_COUNT orders!"
