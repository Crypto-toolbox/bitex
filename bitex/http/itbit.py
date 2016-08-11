"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import ItbitREST

log = logging.getLogger(__name__)


class ITBitHTTP(ItbitREST):
    def __init__(self, userId='', key='', secret='', key_file=''):

        super(ITBitHTTP, self).__init__(userId, key, secret)
        if key_file:
            self.load_key(key_file)

    def ticker(self, pair):
        path = "/markets/%s/ticker" % (pair)
        response = self.query('GET', path)
        return response

    def order_book(self, pair):
        path = "/markets/%s/order_book" % (pair)
        response = self.query('GET', path)
        return response

    def trades(self, pair, since=None):
        if since:
            q = {'since': since}
        else:
            q = {}
        path = '/markets/%s/trades' % pair
        return self.query('GET', path, params=q)

    def balance(self, walletId, currency):
        path = "/wallets/%s/balances/%s" % (walletId, currency)
        response = self._api._query('GET', path, {})
        return response



if __name__ == '__main__':
    uix = ITBitHTTP()
    print(uix.trades('XBTUSD').text)
    print(uix.ticker('XBTUSD').text)
    print(uix.order_book('XBTUSD').text)
