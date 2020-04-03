# Project Cryptos
Process crypto prices using kafka and spark stream combination

## Content
### 1. Summary
### 2. Data Source
### 3. Data Ingestion
### 4. Data Consumption
### 5. Data Storage
### 6. Data Visualization

## Summary
The current plan is to build a streaming pipeline for crypto prices. 
1. ingress crypto currency prices from various free API calls
`CoinMarketCap.py`
    - **Airflow** for orchestration - stay within the daily API call limits
2. stream the incoming data using **Kafka**
3. connect to **Spark** streaming for data processing and analytics
4. store the data in **Cassandra** [connection to Grafana](https://medium.com/@prashantkrgupta28/grafana-cassandra-as-datasource-visualization-of-cassandra-data-712bedfb81fb)
5. **Gafana** dashboard through InfluxDB 

## Data source

### CoinMarketCap.com
Free API calls could be made upto 10,000 per month for an individual with Basic Plan. 
Following the useful [API documentation](https://coinmarketcap.com/api/documentation/v1/), we could get started by 
applying for an API key. 
