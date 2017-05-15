from datetime import datetime
from string import maketrans

import pytz
from django.utils import timezone
from django.utils.dateparse import parse_datetime

int_reais_float_unit = 100000000.0
date_fmt = "%Y-%m-%d %H:%M:%S"

def format_reais(int_reais):

    """
    Given a value of reais as an int (with the same fraction as sathoshis) eg. 100000000.0
    Willl return a formated string
    :return: str of format 'R$ 000.000,00'
    """

    tmp = "R$ {:10,.2f}".format(round(int_reais / int_reais_float_unit, 2))
    return tmp.translate(maketrans(',.', '.,'))

def order_datetime(str):
    dt = datetime.strptime(str, date_fmt)
    return pytz.timezone('UTC').localize(dt)
