"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.http.client import Client
from bitex.api.rest import CoincheckREST

log = logging.getLogger(__name__)


class CoincheckHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = CoincheckREST(key, secret)
        if key_file:
            api.load_key(key_file)
        super(CoincheckHTTP, self).__init__(api, 'Coincheck')

    def order_book(self):
        return self.query('order_books')

    def ticker(self):
        return self.query('ticker')

    def balance(self):
        return self.query('/accounts/balance', authenticate=True)


if __name__ == '__main__':
    uix = CoincheckHTTP()
    print(uix.order_book().text)
    print(uix.ticker().text)
    print(uix.balance().text)
