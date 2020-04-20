from kafka import KafkaProducer, KafkaClient
from kafka.errors import KafkaError
import json


def kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    except Exception as ex:
        print(f'Exception while connecting to Kafka: {ex}')
    finally:
        return _producer


def publish_sms(producer, topic, key, value):
    try:
        producer.send(topic, bytes(key, encoding='utf-8'), bytes(value, encoding='utf-8'))
        producer.flush()
        print('Message published successfully.')
    except Exception as ex:
        print(f'Exception while connecting to Kafka: {ex}')



