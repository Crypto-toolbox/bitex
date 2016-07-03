"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import socket
import json


# Import Third-Party


# Import Homebrew
from bitex.api.itbit import API
from bitex.http.client import Client

log = logging.getLogger(__name__)


class ITBitHTTP(Client):
    def __init__(self, server_addr, key='', secret='', userId='', key_file=''):
        api = API(key, secret, userId)
        if key_file:
            api.load_key(key_file)
        super(ITBitHTTP, self).__init__(server_addr, api, 'ITBit')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(ITBitHTTP, self).send(message)

    def ticker(self, pair):
        path = "/markets/%s/ticker" % (pair)
        response = self._api._query("GET", path, {})
        return response

    def get_order_book(self, pair):
        path = "/markets/%s/order_book" % (pair)
        response = self._api._query("GET", path, {})
        return response

    def get_wallet(self, walletId='', page=1, per_page=50):
        if not walletId:
            q = {'userId': self._api.userId, 'page': page, 'perPage': per_page}

            queryString = self._api._generate_query_string(q)
            path = "/wallets%s" % (queryString)
            response = self._api._query("GET", path, {})
            return response
        else:
            path = "/wallets/%s" % (walletId)
            response = self._api._query("GET", path, {})
            return response

    def create_wallet(self, walletName):
        path = "/wallets"
        response = self._api._query("POST", path, {'userId': self.userId,
                                                    'name': walletName})
        return response

    def balance(self, walletId, currency):
        path = "/wallets/%s/balances/%s" % (walletId, currency)
        response = self._api._query("GET", path, {})
        return response

    def trade_history(self, walletId, last_execution_id='', page=1,
                          per_page=50, range_start=None, range_end=None):
        q = {'lastExecutionId': last_execution_id, 'page': page,
             'perPage': per_page}

        if range_start:
            q['rangeStart'] = range_start
        if range_end:
            q['rangeEnd'] = range_end

        queryString = self._api._generate_query_string(q)
        path = "/wallets/%s/trades%s" % (walletId, queryString)
        response = self._api._query("GET", path, {})
        return response

    def get_wallet_orders(self, walletId):
        q = {}
        queryString = self._api._generate_query_string(q)
        path = "/wallets/%s/orders%s" % (walletId, queryString)
        response = self._api._query("GET", path, {})
        return response

    def place_order(self, walletId, side, currency, amount, price, instrument):
        path = "/wallets/%s/orders/" % (walletId)
        response = self._api._query("POST", path,
                                     {'type': 'limit', 'currency': currency,
                                      'side': side, 'amount': amount,
                                      'price': price, 'instrument': instrument})
        return response

    def create_order_with_display(self, walletId, side, currency, amount, price,
                                  display, instrument):
        path = "/wallets/%s/orders/" % (walletId)
        response = self._api._query("POST", path,
                                     {'type': 'limit', 'currency': currency,
                                      'side': side, 'amount': amount,
                                      'price': price, 'display': display,
                                      'instrument': instrument})
        return response

    def query_order(self, walletId, orderId):
        path = "/wallets/%s/orders/%s" % (walletId, orderId)
        response = self._api._query("GET", path, {})
        return response

    def cancel_order(self, walletId, orderId):
        path = "/wallets/%s/orders/%s" % (walletId, orderId)
        response = self._api._query("DELETE", path, {})
        return response

    def cryptocurrency_withdrawal_request(self, walletId, currency, amount,
                                          address):
        path = "/wallets/%s/cryptocurrency_withdrawals" % (walletId)
        response = self._api._query("POST", path,
                                     {'currency': currency, 'amount': amount,
                                      'address': address})
        return response

    def cryptocurrency_deposit_request(self, walletId, currency):
        path = "/wallets/%s/cryptocurrency_deposits" % (walletId)
        response = self._api._query("POST", path, {'currency': currency})
        return response

    def create_wallet_transfer(self, sourceWalletId, destinationWalletId,
                               amount, currencyCode):
        path = "/wallet_transfers"
        response = self._api._query("POST", path,
                                     {'sourceWalletId': sourceWalletId,
                                      'destinationWalletId': destinationWalletId,
                                      'amount': amount,
                                      'currencyCode': currencyCode})
        return response


if __name__ == '__main__':
    uix = ITBitHTTP(('localhost', 6666))
    print(uix.ticker('XBTUSD'))
