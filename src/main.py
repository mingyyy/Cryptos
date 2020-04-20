from apis.CoinDesk import get_prev
from ingest.producer import publish_sms, kafka_producer
from ingest.consumer import receive_sms


if __name__ == '__main__':
    url = "https://api.coindesk.com/v1/bpi/historical/close.json"
    prices = get_prev(url)
    topic = 'coindesk_past30'

    if prices is not None:
        _producer = kafka_producer()
        for key, val in prices.items():
            publish_sms(_producer, topic, key, str(val))
        if _producer is not None:
            _producer.close()
