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
2. Stream the incoming data using **Kafka**
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
Apache Kafka is a popular choice in this space, known for it's fault tolerance, low latency and high throughput.  

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
4. Start Kafka on each node
```
kafka_2.12-2.4.1$ sudo bin/kafka-server-start.sh config/server.properties &
```

5. Create a topic "my-topic" at one of the node
```
ubuntu@ip-10-0-0-8:~/kafka_2.12-2.4.1$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
```

6. Check the topics from other nodes
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

7. Publish messages from one node.
```
ubuntu@ip-10-0-0-8:~/kafka_2.12-2.4.1$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
```
8. Consume the messages from other nodes
```
ubuntu@ip-10-0-0-4:~/kafka_2.12-2.4.1$ ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning
```