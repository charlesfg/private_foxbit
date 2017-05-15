from django import template

from btc_utils.utils import satoshi_to_btc
from frontend.utils import format_reais

register = template.Library()


@register.filter(is_safe=True)
def s_to_btc(value):
    return satoshi_to_btc(value)

@register.filter(is_safe=True)
def s_rs_format(value):
    return format_reais(value)

@register.filter(is_safe=True)
def order_side(value):
    if value == "1":
        return "Compra"
    elif value == "2":
        return "Venda"
    else:
        return "Treta"

@register.filter(is_safe=True)
def order_status(value):
    if value == "0":
        return "Aberta"
    elif value == "1":
        return "Parcial"
    elif value == "2":
        return "Executada"
    elif value == "4":
        return "Cancelada"
    elif value == "8":
        return "Rejeitada"
    elif value == "A":
        return "Pendente"
    else:
        return "Treta"
