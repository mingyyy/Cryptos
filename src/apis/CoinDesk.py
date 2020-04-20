from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint


def get_current_price(url):
    try:
        # Get current price
        response = Session().get(url)
        data = json.loads(response.text)
        # pprint(data)

        ccy = data['chartName']
        price = data['bpi']['USD']['rate']
        timeStamp = data['time']['updatedISO']
        # print(f'{ccy}: {price} Last update: {timeStamp}')
        return [ccy, price, timeStamp]

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        pprint(e)


def get_prev(url):
    try:
        # Get previous 31 days or user-defined period
        response = Session().get(url)

        data = json.loads(response.text)
        # for key, val in data['bpi'].items():
        #     print(f'Bitcoin: {val:,.2f} date: {key} ')
        return data['bpi']

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        pprint(e)


if __name__ == '__main__':
    # #  current bitcoin price
    # url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    # print(get_current_price(url))

    # historical bitcoin prices of the previous 31 days
    url = "https://api.coindesk.com/v1/bpi/historical/close.json"
    print(get_prev(url))

    # start_date = '2019-01-01'
    # end_date = '2019-04-01'
    # # sample historical bitcoin prices for a period of time: 2013-08-01 to 2013-09-05
    # url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={start_date}&end={end_date}"
    # print(get_prev(url))