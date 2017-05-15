# -*- coding: utf-8 -*-

import hashlib


import hmac
import time
from requests import ConnectionError

import requests
import datetime
import logging
from config import secret, key, CURRENCY, BLINKTRADE_API_URL, BLINKTRADE_API_VERSION, user_agent, BROKER_ID, SYMBOL
import json
logger = logging.getLogger('trade')

def send_msg(msg):
    dt = datetime.datetime.now()
    nonce = str(int((time.mktime( dt.timetuple() )  + dt.microsecond/1000000.0) * 1000000))
    signature = hmac.new( secret,  nonce, digestmod=hashlib.sha256).hexdigest()
    headers = {
        'user-agent': user_agent,
        'Content-Type': 'application/json',
        'APIKey': key,
        'Nonce': nonce,
        'Signature': signature
    }
    url = '%s/tapi/%s/message' % (BLINKTRADE_API_URL, BLINKTRADE_API_VERSION)
    try:
        get = requests.post(url, json=msg, verify=True, headers=headers)
    except ConnectionError as e:
        logger.error("Error on '{}' : {}".format(msg["MsgType"], e))
        return None

    if get.status_code == 200:
        return get.json()
    else:
        logger.error("Error on '{}' : {}".format(msg["MsgType"], get.text))
        return get.status_code


def balance():
  msg = {
    "MsgType": "U2",    # Balance Request
    "BalanceReqID": 1   # An ID assigned by you. It can be any number.  The response message associated with this request will contain the same ID.
  }
  return send_msg(msg)


def orders(page=0, page_size=20, filter_orders=1):
    """

    :param page:
    :param page_size:
    :param filter_orders:
        0 = All
        1 = Open Orders
        2 = Executed
        3 = Canceled
    :return:
    """

    dict_filter = {
        1 : "has_leaves_qty eq 1",
        2 : "has_cum_qty eq 1",
        3 : "has_cxl_qty eq 1",  # Seems not to work
    }

    msg = {
        "MsgType": "U4",  # Balance Request
        "OrdersReqID": 1,
        "Page": page,
        "PageSize": page_size
    }

    if filter_orders > 0 and filter_orders < 4:
        msg["Filter"] = [dict_filter[filter_orders]]

    return send_msg(msg)

def send_order(ClOrdID, Price, OrderQty, Buy):
    """
            ClOrdID	    number	    Unique identifier for Order as assigned by you
            Symbol	    string	    <SYMBOL>
            Side	    string	    “1” = Buy, “2” = Sell
            OrdType	    string	    “2” = Limited
            Price	    number	    Price in satoshis
            OrderQty	number	    Quantity in satoshis
            BrokerID	number	    <BROKER_ID>
    """
    if Buy != "1" and Buy != "2":
        raise ValueError("Wan't buy(1) or sell(2) you put {}".format(Buy))

    msg = {
        "MsgType": "D",
        "ClOrdID": ClOrdID,
        "Symbol": SYMBOL,
        "Side":Buy,
        "OrdType": "2",
        "Price": Price,
        "OrderQty": OrderQty,
        "BrokerID": BROKER_ID
    }
    return send_msg(msg)


def cancel_order(ClOrdID):
    msg = {
        "MsgType": "F",
        "ClOrdID": ClOrdID
    }
    return send_msg(msg)


def reais_to_satoshi(rs_float):
    return int(rs_float * 100000000)

def bitcoin_to_satoshi(bt_float):
    return int(bt_float * 100000000)

def buy_btc():
    return None

def print_pretty(obj):
    print json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))

if __name__ == '__main__':
    #b = send_order(2,reais_to_satoshi(6901.59),bitcoin_to_satoshi(0.00997500),"2")
    #b = cancel_order(1)


    print_pretty(orders(filter_orders=0))


