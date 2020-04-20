import kafka

# connect to Kafka Cluster
cluster = kafka.KafkaClient("52.8.85.143:9092")
topic = "my-topic"
consumer_group = "default_group"
consumer = kafka.KafkaConsumer(cluster, consumer_group, topic)

# consume all messages
for raw in consumer:
    msg = raw.message.value
    print(msg)
