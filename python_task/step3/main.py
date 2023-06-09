from kafka import KafkaProducer, KafkaConsumer
import csv
import os

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'price_data.csv')

def fill_kafka_topic():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            price = row[0] 
            producer.send('main_topic', value=price.encode('utf-8'))
    producer.close()

def get_price_data():
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092', group_id='price_updater')
    consumer.subscribe(['main_topic'])

    for message in consumer:
        price = message.value.decode('utf-8')
        print(price)
    consumer.close()


if __name__ == '__main__':
    fill_kafka_topic()
    get_price_data()
