"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import BTCERest
from bitex.http.client import Client

log = logging.getLogger(__name__)


class BTCEHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = BTCERest(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BTCEHTTP, self).__init__(api, 'BTCE')

    def ticker(self, *pairs):
        if len(pairs) > 1:
            pairs = '-'.join(pairs)
        else:
            pairs = pairs[0]

        return self.query('ticker/%s' % pairs)

    def order_book(self, pair, limit=150):
        q = {'limit': limit}
        return self.query('depth/%s' % pair, params=q)

    def trades(self, pair, limit=150):
        q = {'limit': limit}
        return self.query('trades/%s' % pair, params=q)




if __name__ == '__main__':
    uix = BTCEHTTP(key='a64db1b5779246fb9dd907ab9571acff', secret='c5011fe2731f40ccb52fa32ab76251ba')
    print(uix.ticker('btc_usd', 'btc_rur').text)
    print(uix.order_book('btc_usd').text)
    print(uix.trades('btc_usd').text)

