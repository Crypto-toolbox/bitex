"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import ItbitREST
from bitex.http.client import Client

log = logging.getLogger(__name__)


class ITBitHTTP(Client):
    def __init__(self, key='', secret='', userId='', key_file=''):
        api = ItbitREST(key, secret, userId)
        if key_file:
            api.load_key(key_file)
        super(ITBitHTTP, self).__init__(api, 'ITBit')

    def ticker(self, pair):
        path = "/markets/%s/ticker" % (pair)
        response = self.query(path, {})
        return response

    def get_order_book(self, pair):
        path = "/markets/%s/order_book" % (pair)
        response = self._api._query("GET", path, {})
        return response

    def trades(self, pair, since=None):
        if since:
            q = {'since': since}
        else:
            q = {}
        path = '/markets/%s/trades' % pair
        return self.query(path, q)

    def balance(self, walletId, currency):
        path = "/wallets/%s/balances/%s" % (walletId, currency)
        response = self._api._query("GET", path, {})
        return response



if __name__ == '__main__':
    uix = ITBitHTTP()
    print(uix.trades('XBTUSD').text)
