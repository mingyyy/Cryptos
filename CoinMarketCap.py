# Basic plan
# daily limit: 333, monthly: 10,000
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
from secret import API_KEY

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Bitcoin in USD
parameters = {'id':'1',}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}
session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

  pprint(data)

  symbol = data['data']['1']['symbol']
  price = data['data']['1']['quote']['USD']['price']
  timeStamp = data['data']['1']['quote']['USD']['last_updated']
  marketCap = data['data']['1']['quote']['USD']['market_cap']
  change1h = data['data']['1']['quote']['USD']['percent_change_1h']
  change24h = data['data']['1']['quote']['USD']['percent_change_24h']
  change7d = data['data']['1']['quote']['USD']['percent_change_7d']
  volume24h = data['data']['1']['quote']['USD']['volume_24h']
  supply = data['data']['1']['total_supply']

  print(f'{symbol}: {price} Last update: {timeStamp}')
  print(f'total supply: {supply:,}')
  print(f'market cap: {marketCap:,.2f}')
  print(f'volume in 24 hours: :{volume24h:,.2f}')

except (ConnectionError, Timeout, TooManyRedirects) as e:
  pprint(e)