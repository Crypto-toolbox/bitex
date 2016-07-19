"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.okcoin import API
from bitex.http.client import Client

log = logging.getLogger(__name__)


class OKCoinHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(OKCoinHTTP, self).__init__(api, 'OKCoin')

    def order_book(self, pair):
        q = {'pair': pair}
        return self._query('depth.do', q)

    def ticker(self, pair):
        return self._query('ticker.do', {'symbol': pair})

if __name__ == '__main__':
    uix = OKCoinHTTP()
    print(uix.ticker('btc_usd'))
