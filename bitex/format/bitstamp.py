"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


def http_format_ob(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp, pair = func(self, *args, **kwargs)
        ts = resp['timestamp']
        formatted = []
        for a, b in zip(resp['asks'], resp['bids']):
            ask_p, ask_v = a
            bid_p, bid_v = b
            formatted.append([ts, 'Ask Price', ask_p])
            formatted.append([ts, 'Ask Vol', ask_v])
            formatted.append([ts, 'Bid Price',  bid_p])
            formatted.append([ts, 'Bid Vol', bid_v])
        return [self._format(sent, received, pair, *i) for i in formatted]
    return wrapper
