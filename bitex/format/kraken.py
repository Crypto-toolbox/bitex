"""
Task:
Contains formatter decorators for output data
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


def http_format_ob(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp, pair = func(self, *args, **kwargs)
        formatted = []
        for a, b in zip(resp['result'][pair]['asks'],
                        resp['result'][pair]['bids']):
            ask_p, ask_v, ask_t = a
            bid_p, bid_v, bid_t = b
            formatted.append([ask_t, 'Ask Price', ask_p])
            formatted.append([ask_t, 'Ask Vol', ask_v])
            formatted.append([bid_t, 'Bid Price', bid_p])
            formatted.append([bid_t, 'Bid Vol', bid_v])
        return [self._format(sent, received, pair, *i) for i in formatted]
    return wrapper


