"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import CoincheckREST

log = logging.getLogger(__name__)


class CoincheckHTTP(CoincheckREST):
    def __init__(self, key='', secret='', key_file=''):

        super(CoincheckHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self):
        return self.query('GET', 'order_books')

    def ticker(self):
        return self.query('GET', 'ticker')

    def trades(self):
        return self.query('GET', 'trades')

    def balance(self):
        return self.query('GET', '/accounts/balance', authenticate=True)


if __name__ == '__main__':
    uix = CoincheckHTTP()
    print(uix.order_book().text)

