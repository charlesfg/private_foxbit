import json
import re

from datetime import datetime
import time

d_frmt = r"%Y-%m-%d %H:%M:%S"


def dt_str_to_uts(str):
    """
    Convert the str formatted in the d_frmt format to unix timestamp
    :param str:
    :return:
    """
    dt = datetime.strptime(str, d_frmt)
    return int(time.mktime(dt.timetuple()))


def dt_str_from_ts(ts):
    return datetime.fromtimestamp(ts).strftime(d_frmt)

def uts_from_timestr(t_str, dt_str=None):
    """
    Unix times stamp from time string

    if dt_str define it will generate the diff from that time

    Accepts the format
     (+?|-)int(s|m|h|d|empty)

     Empty assumes seconds

    :param t_str:
    :return:
    """
    t_str.strip()
    pttn = re.compile(r"^(\+?|-)(\d+)(\D?)$")
    m = pttn.match(t_str)

    if not m:
        raise ValueError("Time format not supported")

    sign = 1
    if m.group(1) and m.group(1) == '-':
        sign = -1

    amount = int(m.group(2))
    unit = m.group(3).lower()

    multiplier = None

    if not unit or unit == "s":
        multiplier = 1
    elif unit == "m":
        multiplier = 60
    elif unit == "h":
        multiplier = 60 * 60
    elif unit == "d":
        multiplier = 60 * 60 * 24
    else:
        raise ValueError("Unrecognized {} time specifier".format(unit))

    if dt_str:
        t = dt_str_to_uts(dt_str)
    else:
        t = int(time.time())

    return t + ( sign * amount * multiplier)


def print_pretty(json_data):
    print json.dumps(json_data, indent=2, sort_keys=True)


if __name__ == '__main__':
    print dt_str_from_ts(time.time())
    print int(time.time())
    print dt_str_to_uts("2017-05-11 11:26:40")