"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import OKCoinREST

log = logging.getLogger(__name__)


class OKCoinHTTP(OKCoinREST):
    def __init__(self, key='', secret='', key_file=''):
        super(OKCoinHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair):
        q = {'pair': pair}
        return self.query('GET', '/depth.do', params=q)

    def ticker(self, pair):
        return self.query('GET', '/ticker.do', params={'symbol': pair})

    def trades(self, pair):
        q = {'pair': pair}
        return self.query('GET', '/trades.do', params=q)

if __name__ == '__main__':
    uix = OKCoinHTTP()
    print(uix.ticker('btc_usd').text)

