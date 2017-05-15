# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
import logging

from django.db.models import Model, IntegerField
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import BigIntegerField, CharField, DateTimeField
from django.db.models.fields.related import OneToOneField

from frontend.utils import order_datetime

logger = logging.getLogger('backend')

class Order(Model):
    class Meta:
        managed = True
        app_label = "backend"

    # https://github.com/blinktrade/frontend/wiki/Rest-API#request-open-orders
    OPEN_ORDER = "0"
    EXECUTED_ORDER = "2"
    ORDER_STATUS_CHOICES = (
        (OPEN_ORDER, 'New'),
        ("1", 'Partially filled'),
        (EXECUTED_ORDER, 'Filled'),
        ("4", 'Cancelled'),
        ("8", 'Rejected'),
        ("A", 'Pending New')
    )

    ORDER_SIDE = (
        ("1", "BUY"),
        ("2", "SELL")
    )

    ClOrdId = BigIntegerField(unique=True,null=True)
    OrderId = BigIntegerField(primary_key=True, unique=True)
    CumQty = BigIntegerField()
    OrdStatus = CharField(max_length=1, choices=ORDER_STATUS_CHOICES)
    LeavesQty = BigIntegerField()
    CxlQty = BigIntegerField()
    AvgPx = BigIntegerField()
    Symbol = CharField(max_length=6)
    Side = CharField(max_length=1, choices=ORDER_SIDE, db_index=True)
    OrdType = CharField(max_length=1)
    OrderQty = BigIntegerField()
    # Price per unit in "satoshis" of your local currency
    Price = BigIntegerField()
    # Order date in UTC.
    # will have the format : "2017-05-10 21:52:12"
    OrderDate = DateTimeField(auto_now=False)
    Volume = BigIntegerField()  # Quantity * Price
    TimeInForce = CharField(max_length=1)

    def parse_api_order(self, api_order):
        self.ClOrdId = api_order[0]
        self.OrderId = api_order[1]
        self.CumQty = api_order[2]
        self.OrdStatus = api_order[3]
        self.LeavesQty = api_order[4]
        self.CxlQty = api_order[5]
        self.AvgPx = api_order[6]
        self.Symbol = api_order[7]
        self.Side = api_order[8]
        self.OrdType = api_order[9]
        self.OrderQty = api_order[10]
        self.Price = api_order[11]
        self.OrderDate = order_datetime(api_order[12])
        self.Volume = api_order[13]
        self.TimeInForc = api_order[14]

        pass

    def is_open(self):
        return self.OrdStatus == self.OPEN_ORDER

    @classmethod
    def get_open_orders_ids(cls):

        old_oo = Order.objects.filter(OrdStatus__exact="0")
        oo_ids = []
        for o in old_oo:
            oo_ids.append(o.OrderId)

        logger.debug("Getting {} Opened Orders".format(len(oo_ids)))
        return oo_ids

    @classmethod
    def clean_canceled_orders(cls, canceled_orders_ids):
        for o_id in canceled_orders_ids:
            logger.debug("Deleting the order with Id {} !".format(o_id))
            Order.objects.get(OrderId__exact=o_id).delete()


class Balance(Model):

    BRL = BigIntegerField()
    BRL_locked = BigIntegerField()
    BTC = BigIntegerField()
    BTC_locked = BigIntegerField()
    updated_in = DateTimeField(auto_now_add=True)


class Trade(Model):

    buy = OneToOneField(Order, related_name="trade_buy", on_delete=DO_NOTHING)
    sell = OneToOneField(Order, related_name="trade_sell", on_delete=DO_NOTHING, null=True)
    interest = IntegerField(default=3)
