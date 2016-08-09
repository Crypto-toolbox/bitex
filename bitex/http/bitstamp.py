"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import BitstampREST
from bitex.http.client import Client
log = logging.getLogger(__name__)


class BitstampHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = BitstampREST(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitstampHTTP, self).__init__(api, 'Bitstamp')

    def order_book(self, pair, count=0):
        q = {'pair': pair}
        if count:
            q['count'] = count

        resp = self.query('v2/order_book/%s/' % pair)

        return resp

    def ticker(self, pair):
        response = self.query('v2/ticker/%s/' % pair)
        return response

    def trades(self, pair, t='hour'):
        resp = self.query('v2/transactions/%s/' % pair, data={'time': t})
        return resp

    def balance(self, **kwargs):
        """
        Returns the balance of the exchange account's wallets.
        :param kwargs:
        :return:
        """
        pass

    def orders(self, *args, **kwargs):
        """
        Return open orders.
        :param pair:
        :param kwargs:
        :return:
        """
        pass

    def ledger(self):
        """
        Ledger consists of recent trades, deposits, and withdrawals to and
        from user's account.
        :return:
        """
        pass

    def add_order(self, price, vol, pair, ask_or_bid, order_type='limit',
                  **kwargs):
        """
        Places a bid or ask order of given order type.
        :param prive:
        :param vol:
        :param pair:
        :param ask_or_bid:
        :param order_type:
        :param kwargs:
        :return:
        """
        pass

    def cancel_order(self, uuid):
        """
        cancels an order with the given uuid.
        :param uuid:
        :return:
        """
        pass

    def fees(self):
        """
        Returns fees applicable at exchange.
        :return:
        """
        pass

if __name__ == '__main__':
    uix = BitstampHTTP()
    print(uix.ticker('btcusd').text)
    print(uix.balance('btcusd').text)

