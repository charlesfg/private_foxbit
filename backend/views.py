# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from backend.models import Order, Balance
from btc_utils.utils import satoshi_to_btc

from frontend.utils import format_reais
from foxbit_api import trade

import logging

logger = logging.getLogger('backend')

class ApiBrokerParser:

    def parse_fb_balance(self):

        api_return = trade.balance()
        resp = api_return['Responses']
        if len(resp) == 0:
            logger.error("Api returned empty. Reason: {} : {}".format(api_return['Status'], api_return['Description']))
            return {}
        balance = resp[0]['4']

        m_bal = Balance()
        m_bal.BRL = balance['BRL']
        m_bal.BRL_locked = balance['BRL_locked']
        m_bal.BTC = balance['BTC']
        m_bal.BTC_locked = balance['BTC_locked']
        m_bal.save()

        b = {

            'BRL': format_reais(balance['BRL']),
            'BRL_locked': format_reais(balance['BRL_locked']),
            'BRL_free': format_reais(balance['BRL'] - balance['BRL_locked']),

            'BTC': satoshi_to_btc(balance['BTC']),
            'BTC_locked': satoshi_to_btc(balance['BTC_locked']),
            'BTC_free': satoshi_to_btc(balance['BTC'] - balance['BTC_locked']),

        }

        return b

    def update_orders(self, force=False):

        pg = 0

        # Get the open orders to check if anyone was canceled
        old_oo_ids = Order.get_open_orders_ids()
        oo_ids = []

        # Just a placeholder to do not have an empty list
        order_list = [1]

        while order_list:
            orders = trade.orders(filter_orders=0, page=pg)
            pg += 1
            o_resp = orders["Responses"][0]
            ret_pg = int(o_resp["Page"])
            order_list = o_resp["OrdListGrp"]
            for o in order_list:
                m = Order()
                m.parse_api_order(o)
                if m.is_open():
                    oo_ids.append(m.OrderId)
                m.save()

        # Any order that was open before but does not exists anymore was canceled
        canceled_orders = filter(lambda x: x in oo_ids, old_oo_ids)
        Order.clean_canceled_orders(canceled_orders)




