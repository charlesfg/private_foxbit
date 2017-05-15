# -*- coding: utf-8 -*-

import hashlib


import hmac
import json
import time
from requests import ConnectionError

import requests
import datetime
import logging

from tabulate import tabulate

from config import secret, key, CURRENCY, BLINKTRADE_API_URL, BLINKTRADE_API_VERSION, user_agent, BROKER_ID, SYMBOL

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


def orders(page=0, page_size=20):
    msg = {
        "MsgType": "U4",  # Balance Request
        "OrdersReqID": 1,
        "Page": page,
        "PageSize": page_size

    }
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

def satoshi_to_bitcoin(s_int):
    return float(s_int / 100000000.0)

def reais_from_api(r_int, round_to_2dec=False):
    if round_to_2dec:
        return round(float(r_int / 100000000.0),2)
    return float(r_int / 100000000.0)

def bitcoin_to_satoshi(bt_float):
    return int(bt_float * 100000000)


def buy_btc():
    return None

def h_balance():
    bal = balance()
    bal_info = bal['Responses'][0]['4']
    print """
    R$:
        Disponível  R$  {:.2f}
        Travado     R$  {:.2f}

    BitCoins:
        Disponível  BTC {}
        Travado     BTC {}
    """.format(
        reais_from_api(bal_info['BRL']),
        reais_from_api(bal_info['BRL_locked']),
        satoshi_to_bitcoin(bal_info['BTC']),
        satoshi_to_bitcoin(bal_info['BTC_locked'])
        )
    pass




def split_orders():
    """
    Return tuple a,b,c
    a = open orders
    b = executed orders
    c = columns name

    :return:
    """

    j = orders()
    orders_data = j["Responses"][0]
    orders_list = orders_data["OrdListGrp"]
    open_orders = filter(lambda x: x[3] == '0', orders_list)
    executed_orders = filter(lambda x: x[3] == '2', orders_list)
    columns_names = orders_data["Columns"]

    return open_orders, executed_orders, columns_names

def open_orders():
    return split_orders()[0]


def h_orders(all=False):
    o,e,c = split_orders()
    print "Open Orders"
    print tabulate(o, c, tablefmt="grid")
    if all:
        print "Executed Orders"
        print tabulate(e, c, tablefmt="grid")


if __name__ == '__main__':
    #b = send_order(2,reais_to_satoshi(6901.59),bitcoin_to_satoshi(0.00997500),"2")
    #b = cancel_order(1)
    h_balance()
    h_orders()
    #print open_orders()


