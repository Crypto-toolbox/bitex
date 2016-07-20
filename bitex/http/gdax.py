"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging


# Import Third-Party
from bitex.api.rest import GDAXRest
from bitex.http.client import Client

# Import Homebrew

log = logging.getLogger(__name__)


class GdaxHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = GDAXRest(key, secret)
        if key_file:
            api.load_key(key_file)
        super(GdaxHTTP, self).__init__(api, 'GDAX')

    def order_book(self, pair):
        return self.query('products/%s/book' % pair, authenticate=True)

    def ticker(self, pair):
        return self.query('products/%s/ticker' % pair, authenticate=True)

    def trades(self, pair):
        return self.query('/products/%s/trades' % pair, authenticate=True)

    def accounts(self):
        return self.query('accounts', authenticate=True)


if __name__ == '__main__':
    uix = GdaxHTTP()
    print(uix.order_book('BTC-USD').text)
    print(uix.ticker('BTC-USD').text)
    print(uix.trades('BTC-USD').text)
    print(uix.accounts().text)
