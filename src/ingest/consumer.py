import json
from kafka import KafkaConsumer


def receive_sms(topic):
    consumer = KafkaConsumer(topic,
                            bootstrap_servers=['localhost:9092'],
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            consumer_timeout_ms=1000)
                         # value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for sms in consumer:
        # both to string
        price = sms.key.decode('utf-8')
        date = sms.value.decode('utf-8')
        print(date, price)

    if consumer is not None:
        consumer.close()


if __name__ == '__main__':
    topic = 'coindesk_past30'
    receive_sms(topic)