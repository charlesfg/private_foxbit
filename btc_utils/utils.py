
# Number of satoshis in a BTC
btc_satoshi = 100000000
btc_satoshi_f = 100000000.0


def ensure_float(isfloat):
    try:
        if type(isfloat) == float:
            return True
        if type(isfloat) == str and type(isfloat) == float:
            return True
    except:
        raise ValueError("Not a float {}".format(isfloat))

def reais_to_satoshi(rs_float):
    ensure_float(rs_float)
    return int(rs_float * btc_satoshi)

def bitcoin_to_satoshi(bt_float):
    ensure_float(bt_float)
    return int(bt_float * btc_satoshi)

def satoshi_to_btc(st_int):
    return float(st_int/btc_satoshi_f)