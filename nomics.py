import urllib.request
from secret import Nomics_API_KEY
from pprint import pprint

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = f"https://api.nomics.com/v1/currencies/ticker?key={Nomics_API_KEY}" \
      f"&ids=BTC,ETH,XRP&interval=1d,30d&convert=USD"
# BTC, ETH and XRP each is a dictionary, in a list
session = Session()
# pprint(urllib.request.urlopen(url).read())
try:
    response = session.get(url)

    data = json.loads(response.text)
    # data[0] BTC, data[1] ETH, data[2] XRP
    pprint(data[0])
    symbol = data[0]['symbol']
    price = data[0]['price']
    timeStamp = data[0]['price_date']
    supply = float(data[0]['circulating_supply'])
    marketCap = float(data[0]['market_cap'])

    print(f'{symbol}: {price} Last update: {timeStamp}')
    print(f'total supply: {supply:,}')
    print(f'market cap: {marketCap:,}')

except (ConnectionError, Timeout, TooManyRedirects) as e:
    pprint(e)

