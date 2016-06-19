"""
Task:
Contains formatter decorators for output data
"""

# Import Built-Ins
import logging
from itertools import zip_longest
# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


def http_format_ob(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp, pair = func(self, *args, **kwargs)
        formatted = []
        for a, b in zip_longest(resp['result'][pair]['asks'],
                                resp['result'][pair]['bids']):

            if a is not None:
                ask_p, ask_v, ask_t = a
                formatted.append([ask_t, 'Ask Price', ask_p])
                formatted.append([ask_t, 'Ask Vol', ask_v])

            if b is not None:
                bid_p, bid_v, bid_t = b
                formatted.append([bid_t, 'Bid Price', bid_p])
                formatted.append([bid_t, 'Bid Vol', bid_v])

        return [self._format(sent, received, pair, *i) for i in formatted]
    return wrapper


def http_format_time(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp = func(self, *args, **kwargs)
        formatted = [None, 'Server Time', resp['result']['unixtime']]
        return self._format(sent, received, None, *formatted)
    return wrapper


def http_format_assets(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp = func(self, *args, **kwargs)
        formatted = []
        for asset in resp['result']:
            for key in resp['result'][asset]:
                formatted.append([sent, received, asset, key,
                                  resp['result'][asset][key]])
        return formatted
    return wrapper


def http_format_asset_pairs(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp = func(self, *args, **kwargs)
        formatted = []
        for asset in resp['result']:
            for key in resp['result'][asset]:
                print(key)
                if key != 'fees' and key != 'fees_maker':
                    formatted.append([sent, received, asset, key,
                                      resp['result'][asset][key]])
                else:
                    print("FEES!")
                    field = 'Maker Fee ' if key == 'fee_maker' else 'Taker Fee '
                    for i in range(len(resp['result'][asset][key])):
                        formatted.append([sent, received, asset,
                                          field+'Tier %s Vol' % str(i+1),
                                          resp['result'][asset][key][i][0]])

                        formatted.append([sent, received, asset,
                                          field + 'Tier %s' % str(i + 1),
                                          resp['result'][asset][key][i][1]])
        return formatted
    return wrapper

