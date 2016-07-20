"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import OKCoinREST
from bitex.http.client import Client

log = logging.getLogger(__name__)


class OKCoinHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = OKCoinREST(key, secret)
        if key_file:
            api.load_key(key_file)
        super(OKCoinHTTP, self).__init__(api, 'OKCoin')

    def order_book(self, pair):
        q = {'pair': pair}
        return self.query('/depth.do', params=q)

    def ticker(self, pair):
        return self.query('/ticker.do', params={'symbol': pair})

    def trades(self, pair):
        q = {'pair': pair}
        return self.query('/trades.do', params=q)

if __name__ == '__main__':
    uix = OKCoinHTTP()
    print(uix.ticker('btc_usd').text)
    print(uix.trades('btc_usd').text)
    print(uix.order_book('btc_usd').text)
