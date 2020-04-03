from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint

# current bitcoin price
url = "https://api.coindesk.com/v1/bpi/currentprice.json"
# historical bitcoin prices of the previous 31 days
url_historical_30 = "https://api.coindesk.com/v1/bpi/historical/close.json"
# sample historical bitcoin prices for a period of time
url_periodical = "https://api.coindesk.com/v1/bpi/historical/close.json?start=2013-08-01&end=2013-09-05"
session = Session()

try:
    # Get previous 31 days
    # response = session.get(url_historical_30)

    # Get self-defined period
    response = session.get(url_periodical)

    data = json.loads(response.text)
    for key, val in data['bpi'].items():
        print(f'Bitcoin: {val:,.2f} date: {key} ')

    # pprint(data)

    # Get current price
    # response = session.get(url)
    # data = json.loads(response.text)
    # ccy = data['chartName']
    # price = data['bpi']['USD']['rate']
    # timeStamp = data['time']['updatedISO']
    # print(f'{ccy}: {price} Last update: {timeStamp}')

except (ConnectionError, Timeout, TooManyRedirects) as e:
    pprint(e)