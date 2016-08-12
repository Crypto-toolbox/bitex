"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import BitfinexREST


log = logging.getLogger(__name__)


class BitfinexHTTP(BitfinexREST):
    def __init__(self, key='', secret='', key_file=''):

        super(BitfinexHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair, limit_orders=50, aggregrate=True):
        q = {'limit_asks': limit_orders, 'limit_bids': limit_orders}
        if not aggregrate:
            q['group'] = 0
        return self.query('GET', '/book/%s/' % pair, params=q)

    def ticker(self, pair):
        return self.query('GET', "pubticker/%s" % pair)

    def trades(self, pair, start_time=None, limit_trades=False):
        q = {'limit_trades': limit_trades}
        if start_time:
            q['timestamp'] = start_time
        return self.query('GET', 'trades/%s' % pair, params=q)

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
    uix = BitfinexHTTP()
    print(uix.ticker('ltcbtc').text)
