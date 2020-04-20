import json
from kafka import KafkaConsumer


def receive_sms(topic):
    consumer = KafkaConsumer(topic,
                            bootstrap_servers=['localhost:9092'],
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            api_version=(0,10),
                            consumer_timeout_ms=1000)
                         # value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for sms in consumer :
        print(sms)

    if consumer is not None:
        consumer.close()