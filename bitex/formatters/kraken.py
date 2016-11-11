"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew

log = logging.getLogger(__name__)


def trade(data):
    return data['result']['txid']


def order_book(data, *args, **kwargs):
    pair = args[1]
    forex = ['EUR', 'USD', 'GBP', 'JPY', 'CAD']
    if len(pair) == 6:
        base_cur = pair[:3]
        quote_cur = pair[3:]
        if base_cur.upper() in forex:
            base_cur = 'Z' + base_cur
        else:
            base_cur = 'X' + base_cur

        if quote_cur.upper() in forex:
            quote_cur = 'Z' + quote_cur
        else:
            quote_cur = 'X' + quote_cur
        return data['result'][base_cur+quote_cur]
    else:
        return data['result'][pair]


def cancel(data):
    if int(data['result']['count']) == 1:
        return True
    else:
        return False
