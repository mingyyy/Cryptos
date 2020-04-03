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


## Data ingestion