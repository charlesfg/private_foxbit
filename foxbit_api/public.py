import hashlib
import hmac
import time
from requests.exceptions import ConnectionError

import requests
import datetime
import logging
from config import secret, key, CURRENCY, BLINKTRADE_API_URL, BLINKTRADE_API_VERSION

logger = logging.getLogger('public')

def send_msg(msg):
  dt = datetime.datetime.now()
  nonce = str(int((time.mktime( dt.timetuple() )  + dt.microsecond/1000000.0) * 1000000))
  signature = hmac.new( secret,  nonce, digestmod=hashlib.sha256).hexdigest()
  headers = {
    'user-agent': 'blinktrade_tools/0.1',
    'Content-Type': 'application/json',
    'APIKey': key,
    'Nonce': nonce,
    'Signature': signature
  }
  url = '%s/tapi/%s/message' % (BLINKTRADE_API_URL, BLINKTRADE_API_VERSION)
  return requests.post(url, json=msg, verify=True, headers=headers).json()


def get_pub_ep_result(param):

    url = '%s/api/%s/%s/%s?crypto_currency=BTC' % (BLINKTRADE_API_URL, BLINKTRADE_API_VERSION, CURRENCY, param)

    try:
        get = requests.get(url, verify=True)
    except ConnectionError as e:
        logger.error("Error on '{}' : {}".format(param, e))
        return None
    if get.status_code == 200:
        return get.json()
    else:
        logger.error("Error on '{}' : {}".format(param, get.text))
        return get.status_code


def ticker():
    return get_pub_ep_result('ticker')

def orderbook():
    return get_pub_ep_result('orderbook')


if __name__ == '__main__':
    print ticker()
    #print orderbook()

