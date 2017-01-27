# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class KrknFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        tickers = []
        for k in data['result']:
            d = data['result'][k]
            tickers.append((d['b'][0], d['a'][0], d['h'][1], d['l'][1], d['o'],
                           None, d['c'][0], d['v'][1], d['TimeStamp']))
        if len(tickers) > 1:
            return tickers
        else:
            return tickers[0]

    @staticmethod
    def order(data, *args, **kwargs):
        if not data['error']:
            return data['result']['txid']
        else:
            return False

    @staticmethod
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

    @staticmethod
    def cancel(data, *args, **kwargs):
        if int(data['result']['count']) == 1:
            return True
        else:
            return False
