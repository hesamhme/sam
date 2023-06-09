import pandas as pd
import redis
import json
import os
import csv

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'price_data.csv')

df = pd.read_csv(file_path)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

for index, row in df.iterrows():
    time = str(row['Time'])
    stock = row['Stock']
    price = row['Price']

    formatted_time = f'{str(time).zfill(6)[:2]}:{str(time).zfill(6)[2:4]}:{str(time).zfill(6)[4:6]}'

    price_history = redis_client.get(stock)

    if price_history:
        price_history = json.loads(price_history)
    else:
        price_history = {}

    if 'time' in price_history:
        price_history['time'].append(formatted_time)
        price_history['price'].append(price)
    else:
        price_history['time'] = [formatted_time]
        price_history['price'] = [price]
    redis_client.set(stock, json.dumps(price_history))

    print(f"Updated stock '{stock}' at time '{formatted_time}' with price '{price}'")
#not dockerize yet!