# Project Cryptos
Process crypto prices using kafka and spark stream combination

## Table of Content
### Section 1. [Summary](#summary)
### Section 2. [Data Source](#data-source)
### Section 3. [Data Ingestion](#data-ingestion)
### Section 4. [Data Consumption](#data-consumption)
### Section 5. [Data Storage](#data-storage)
### Section 6. [Data Visualization](#data-visualization)
### Section 7. [Data Orchestration](#data-orchestration)

## Summary
The current plan is to build a streaming pipeline for crypto prices. 
1. Ingress crypto currency prices from various free API calls, e.g.
`CoinMarketCap.py`
    - **Airflow** for orchestration to stay within the daily API call limits
2. Ingest the incoming data using **Kafka**, with data possibly to be consumed by multiple applications.
    - through a messaging system with producers and consumers
    ```
    - ingest
        - producer.py
        - cosumer.py
    ```

    - through kafka streaming. To avoid using Java/Scala, we could use the argparse library in python to wrap the bash comments.
    ```
    - ingest
        - kafka_parsar.py
        - IngestData.py
    ```
3. Connect to **Spark** streaming for data processing and analytics
4. Store the data in **Cassandra** ([connection to Grafana](https://medium.com/@prashantkrgupta28/grafana-cassandra-as-datasource-visualization-of-cassandra-data-712bedfb81fb))
5. **Grafana** dashboard through **InfluxDB**? 

## Data source
- ### CoinMarketCap.com
Free API calls could be made upto 10,000 per month for an individual with the Basic Plan. 
Following the useful [API documentation](https://coinmarketcap.com/api/documentation/v1/), we could get started by 
applying for an API key. 

From latest quotes endpoint, we could retrieve the latest price, market cap, volume and price changes for bitcoin. 
Note that some endpoints are not available for Basic Plan users. 

- ### CoinDesk.com
Disclaimer: [Powered by CoinDesk](https://www.coindesk.com/price/bitcoin)!!!

Thanks to CoinDesk, we have quick access to their BPI(Bitcoin Price Index) data; current prices in USD, GBP and EUR and historical prices in USD.

- ### BitcoinAverage.com


## Data ingestion
Imagine we have a influx of data in real time or near real time, we would have to pass them through as soon as possible.
Apache Kafka is a popular choice in this space, known for it's fault tolerance, low latency and high throughput, 
independent from the Hadoop ecosystem. 
 

#### Kafka Setup
1. Pegasus up a Spark Cluster and ZooKeeper (1 Master and 3 Nodes)
2. Install Kafta on each node
    - Download the latest version `$wget https://downloads.apache.org/kafka/2.4.1/kafka_2.12-2.4.1.tgz`
    - Unzip the tar file `$tar -xzf kafka_2.12-2.4.1.tgz`
    - Get to the kafka file `$cd kafka_2.12-2.4.1`
3. Configure Kafka on each node
    - Change the broker ID from 0 to 3 (first node = 0, second node = 1, etc)
    ```
       # The id of the broker. This must be set to a unique integer for each broker.
       broker.id=0 
    ```
    - Change the `localhost` to `public_dns` of the 
    ```
        # Zookeeper connection string (see zookeeper docs for details).
        # This is a comma separated host:port pairs, each corresponding to a zk
        # server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
        # You can also append an optional chroot string to the urls to specify the
        # root directory for all kafka znodes.
        zookeeper.connect=localhost:2181
    ```
    - Setup JMX port in `/usr/local/kafka/bin/kafka-server-start.sh`. 
    Add the following on the top of the file after all the comments
    
    `export JMX_PORT=${JMX_PORT:-9999}`
4. Start Zookeeper (if it's not already done through pegasus) and Kafka on each node
```
bin/zookeeper-server-start.sh config/zookeeper.properties &

kafka_2.12-2.4.1$ sudo bin/kafka-server-start.sh config/server.properties &
```
Now kafka should be running and we can start sending messages

* Create a topic "my-topic" at one of the node. The length of Kafka topic name should not exceed 249. 
```
ubuntu@ip-10-0-0-8:~/kafka_2.12-2.4.1$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
```

* Check the topics from other nodes
```
ubuntu@ip-10-0-0-5:~/kafka_2.12-2.4.1$  ./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-topic

Topic: my-topic06	PartitionCount: 2	ReplicationFactor: 3	Configs: 
	Topic: my-topic06	Partition: 0	Leader: 2	Replicas: 2,3,0	Isr: 2,3,0
	Topic: my-topic06	Partition: 1	Leader: 3	Replicas: 3,0,1	Isr: 3,0,1
```

- *Leader* is the node responsible for all reads and writes for the given partition. 
    Each node will be the leader for a randomly selected portion of the partitions
- *Replicas* is the list of nodes that replicate the log for this partition regardless of whether they are the leader or even if they are currently alive.
- *Isr* is the set of “in-sync” replicas. 

This is the subset of the replicas list that is currently alive and caught-up to the leader

* Publish messages from one node.
```
ubuntu@ip-10-0-0-8:~/kafka_2.12-2.4.1$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
```
After the `>` prompt, type the message.

* Consume the messages from other nodes
```
ubuntu@ip-10-0-0-4:~/kafka_2.12-2.4.1$ ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning
```
You should be able to see the messages that you typed from another terminal.

#### Kafka connector
1. under config, modify `connect-file-standalone`, `connect-file-sink.properties` and `connect-file-source.properties` files
2. JSON file for kafka producer, where kafka reads the messages line by line

#### [Kafka-Python](https://kafka-python.readthedocs.io/en/master/index.html)

The latest version of this open source project is compatible with python 3.7 and kafka 2.4. 
`pip install kafka-python` to get the latest. 


### Kafka Streaming
TBC


## Data Consumption
Once we have the data ingested through Kafka, Spark could work its magic. 
Apache Spark is an open source project known for it's fast in-memory computation, support for Java/Scala/Python,
as well as high level tools, e.g. Spark Streaming, Spark SQL and MLlib. Spark Streaming is based on DStream which is 
represented by a continuous series of RDDs. Unlike Kafka, Spark streaming is not exactly real-time but in micro-batches.

### Structured streaming
Introduced in Spark 2.0, Spark Structured Streaming is built on top of Spark SQL with SparkSession as it's entry point, 
which uses DataFrames/Datesets API. Same as Spark Streaming, Structured Streaming also uses micro-batching. However, 
the latter one offers exactly-once delivery with very low latency. 

Simply for the ease of use and Python API support with Kafka, in this project we choose the Structured streaming in Spark.
#### Window Operations on Event Time
Window function is easily applied on DataFrames by aggregating over a sliding event-time window. For example, if we want to count 
words within 10-min window, every 5 minutes. 
```
windowedCounts = words.groupBy(
    window(words.timestamp, "10 minutes", "5 minutes")
    words.word
).count()
```

### Structured streaming + Kafka
Following the [Structured Streaming + Kafka Integration Guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
(Kafka broker version 0.10.0 or higher). Please note that as of April, 20, Spark Streaming + Kafka Integration for Kafka 0.10 and higher version 
doesn't support Python while the lower version which does is [deprecated as of Spark 2.3.0](https://spark.apache.org/docs/2.4.5/streaming-kafka-integration.html).

1. Linking. Add the following in deployment
```
groupId = org.apache.spark
artifactId = spark-streaming-kafka-0-10_2.12
version = 2.4.5
```

2. Reading data from Kafak. Import `KafkaUtils`
```
from pyspark.streaming.kafka import KafkaUtils
directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {'metadata.broker.list': brokers})

```
Note: by default, the Python API will decode Kafka data as UTF8 encoded strings. 

3. Deploying. 
```
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-2-12_2.12:2.4.5
```

## Data Storage

### Install Cassandra on Ubuntu 18.04 from Debian packages
1. Start an EC2 instance with SSH enabled for your IP
2. Access your instance through SSH
3. Follow the official guide on [apache foundation](https://cassandra.apache.org/download/) page
    - Check Java version `java -version`. If no Java installed, use the following to install java
    ```
    sudo apt update
    sudo apt install openjdk-8-jdk openjdk-8-jre
    ```
    - Add the Apache repository of Cassandra to `/etc/apt/sources.list.d/cassandra.sources.list`
    ```
    echo "deb https://downloads.apache.org/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
    ```
    - Add the Apache Cassandra repository keys:
    ```
    curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -
    ```
    - Update the repositories:
    ```
    sudo apt-get update
    ```
    - Add the public key if encounter the error
    ```
    sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA
    ```
    - Update the repositories again
    - Install Cassandara:
    ```
    sudo apt-get install cassandra
    ```
    - Monitor the progress of the startup with:
    ```
    tail -f /var/log/cassandra/system.log
    ```

4. To start Cassandra
```
sudo service cassandra start
```
5. To stop Cassandra
```
sudo service cassandra stop
```
6. To verify the installation
```
sudo service cassandra status
```
7. Connect to the database with:
```
cqlsh
```
Because no specific node is given, the shell then indicates that you are connected to "Test Cluster", which
is the cluster of one node at localhost set up by default. 
