import pandas as pd
import redis
import json
import concurrent.futures
import time
import os

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'price_data.csv')
# Simulated performance metric calculation (takes 3 seconds)
def calculate_performance(stock_price):
    time.sleep(3)
    return 0

# Read the price data from the CSV file
df = pd.read_csv(file_path)

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Helper function to calculate and update performance for a stock
def calculate_and_update_performance(stock, price):
    # Calculate performance metric
    performance = calculate_performance(price)

    # Retrieve the existing stock data from Redis
    stock_data = redis_client.get(stock)

    if stock_data:
        # If stock data exists, decode it from JSON
        stock_data = json.loads(stock_data)
    else:
        # If no stock data exists, initialize it as an empty dictionary
        stock_data = {}

    # Update the performance field in the stock data
    stock_data['performance'] = performance

    # Update the stock data in Redis as JSON
    redis_client.set(stock, json.dumps(stock_data))

    print(f"Updated performance for stock '{stock}' with value '{performance}'")

if __name__ == '__main__':
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        time = str(row['Time'])
        stock = row['Stock']
        price = row['Price']

        # Format the time to match the desired format in Redis
        formatted_time = f'{str(time).zfill(6)[:2]}:{str(time).zfill(6)[2:4]}:{str(time).zfill(6)[4:6]}'

        # Retrieve the existing price history for the stock
        price_history = redis_client.get(stock)

        if price_history:
            # If price history exists, decode it from JSON
            price_history = json.loads(price_history)
        else:
            # If no price history exists, initialize it as an empty dictionary
            price_history = {}

        # Check if the price has changed
        if formatted_time not in price_history.get('time', []):
            # Add the current price and time to the price history
            price_history.setdefault('time', []).append(formatted_time)
            price_history.setdefault('price', []).append(price)

            # Update the price history in Redis as JSON
            redis_client.set(stock, json.dumps(price_history))

            # Calculate and update performance using parallelism
            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.submit(calculate_and_update_performance, stock, price)

            print(f"Updated stock '{stock}' at time '{formatted_time}' with price '{price}' and initiated performance calculation")
        else:
            print(f"Ignored stock '{stock}' at time '{formatted_time}' with price '{price}' as it has not changed")
