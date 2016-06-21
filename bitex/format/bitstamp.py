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


def http_format_ticker(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp, pair = func(self, *args, **kwargs)
        formatted = []
        ts = resp['timestamp']
        formatted.append(self._format(sent, received, pair,
                                      ts, 'Ask Price', resp['ask']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Bid Price', resp['bid']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Last Price', resp['last']))

        formatted.append(self._format(sent, received, pair, ts,
                                      'Trade Volume 24h', resp['volume']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'VWAP 24h', resp['vwap']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Low 24h', resp['low']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'High 24h', resp['high']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Open Price', resp['open']))

        return formatted
    return wrapper