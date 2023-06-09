from confluent_kafka import Producer

kafka_bootstrap_servers = 'localhost:9092'

kafka_producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})
