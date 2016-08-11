"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging


# Import Third-Party
from bitex.api.rest import GDAXRest

# Import Homebrew

log = logging.getLogger(__name__)


class GdaxHTTP(GDAXRest):
    def __init__(self, passphrase='', key='', secret='', key_file=''):

        super(GdaxHTTP, self).__init__(passphrase, key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair):
        return self.query('GET', 'products/%s/book' % pair, authenticate=True)

    def ticker(self, pair):
        return self.query('GET', 'products/%s/ticker' % pair, authenticate=True)

    def trades(self, pair):
        return self.query('GET', '/products/%s/trades' % pair, authenticate=True)

    def accounts(self):
        return self.query('GET', 'accounts', authenticate=True)


if __name__ == '__main__':
    uix = GdaxHTTP()
    print(uix.order_book('BTC-USD').text)

