# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from backend.models import Order
from backend.views import ApiBrokerParser

logger = logging.getLogger('frontend')


class Index(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        p = ApiBrokerParser()
        context['balance'] = p.parse_fb_balance()
        return context




class OrderListView(ListView):
    model = Order
    template_name = 'frontend/orders.html'

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        p = ApiBrokerParser()
        #p.update_orders()
        return context
