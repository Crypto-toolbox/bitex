"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import BTCERest


log = logging.getLogger(__name__)


class BTCEHTTP(BTCERest):
    def __init__(self, key='', secret='', key_file=''):
        super(BTCEHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def ticker(self, *pairs):
        if len(pairs) > 1:
            pairs = '-'.join(pairs)
        else:
            pairs = pairs[0]

        return self.query('GET', 'ticker/%s' % pairs)

    def order_book(self, pair, limit=150):
        q = {'limit': limit}
        return self.query('GET', 'depth/%s' % pair, params=q)

    def trades(self, pair, limit=150):
        q = {'limit': limit}
        return self.query('GET', 'trades/%s' % pair, params=q)




if __name__ == '__main__':
    uix = BTCEHTTP(key='a64db1b5779246fb9dd907ab9571acff', secret='c5011fe2731f40ccb52fa32ab76251ba')
    print(uix.ticker('btc_usd', 'btc_rur').text)
    print(uix.order_book('btc_usd').text)
    print(uix.trades('btc_usd').text)

