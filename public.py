import hashlib
import hmac
import re
import time
from requests.exceptions import ConnectionError

import requests
import datetime
import logging

from tabulate import tabulate

from config import secret, key, CURRENCY, BLINKTRADE_API_URL, BLINKTRADE_API_VERSION, CRYPTO_CURRENCY
from private_foxbit.utils import print_pretty, dt_str_from_ts, uts_from_timestr

logger = logging.getLogger('public')


def get_pub_ep_result(method, params={}):

    params["crypto_currency"]=CRYPTO_CURRENCY

    qp = []
    for k,v in params.iteritems():
        qp.append("{}={}".format(k,v))

    url = '%s/api/%s/%s/%s?%s' % (BLINKTRADE_API_URL, BLINKTRADE_API_VERSION, CURRENCY, method, "&".join(qp))

    try:
        get = requests.get(url, verify=True)
    except ConnectionError as e:
        logger.error("Error on '{}' : {}".format(method, e))
        return None
    if get.status_code == 200:
        return get.json()
    else:
        logger.error("Error on '{}' : {}".format(method, get.text))
        return get.status_code


def ticker():
    return get_pub_ep_result('ticker')

def orderbook():
    return get_pub_ep_result('orderbook')

def trades(since=None, limit=None):
    if not since and not limit:
        return get_pub_ep_result('trades')
    else:
        d = {}
        if since:
            d["since"] = since
        if limit:
            d["limit"] = limit
        return get_pub_ep_result('trades', d)


def trades_for_tabulate(trades, convert_date=True):

    columns = trades[0].keys()
    columns.sort()

    all_trades = []

    for t in trades:
        trade_array = []
        for c in columns:
            if c == "date" and convert_date:
                trade_array.append(dt_str_from_ts(t[c]))
            else:
                trade_array.append(t[c])


        all_trades.append(trade_array)

    return all_trades, columns





def h_trades(*args, **kwargs):
    t = trades(*args, **kwargs)
    if not t:
        logger.info("No trades to show")
        return
    all_t, c = trades_for_tabulate(t)
    print tabulate(all_t,c,tablefmt="grid")


if __name__ == '__main__':
    #print ticker()
    #print orderbook()
    h_trades(since=uts_from_timestr("-15m"))


