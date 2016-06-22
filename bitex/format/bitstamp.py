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


def http_format_hourly_ticker(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp, pair = func(self, *args, **kwargs)
        formatted = []
        ts = resp['timestamp']
        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly Ask Price', resp['ask']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly Bid Price', resp['bid']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly Last Price', resp['last']))

        formatted.append(self._format(sent, received, pair, ts,
                                      'Hourly Trade Volume 24h', resp['volume']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly VWAP 24h', resp['vwap']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly Low 24h', resp['low']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly High 24h', resp['high']))

        formatted.append(self._format(sent, received, pair,
                                      ts, 'Hourly Open Price', resp['open']))

        return formatted
    return wrapper


def http_format_trades(func):
    def wrapper(self, *args, **kwargs):
        sent, received, resp, pair = func(self, *args, **kwargs)
        formatted = []
        for trade in resp:

            ts = trade['date']
            formatted.append(self._format(sent, received, pair,
                                          ts, 'Order Price', trade['price']))

            formatted.append(self._format(sent, received, pair,
                                          ts, 'Order TID', trade['tid']))

            formatted.append(self._format(sent, received, pair,
                                          ts, 'Order Size', trade['amount']))

            formatted.append(self._format(sent, received, pair, ts,
                                          'Order Type', trade['type']))

        return formatted
    return wrapper