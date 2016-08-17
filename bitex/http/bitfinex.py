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

    def order_book(self, pair, **kwargs):
        if kwargs:
            q = kwargs
        else:
            q = {}

        r = self.query('GET', '/book/%s/' % pair, params=q).json()
        asks = [(str(order['price']), str(order['amount']), str(order['timestamp'])) for order in r['asks']]
        bids = [(str(order['price']), str(order['amount']), str(order['timestamp'])) for order in r['bids']]
        return {'asks': asks, 'bids': bids}

    def ticker(self, pair):
        r = self.query('GET', "pubticker/%s" % pair).json()
        return {'last': r['last_price'],
                '24h Vol': r['volume'],
                'ask': r['ask'],
                'bid': r['bid'],
                'timestamp': r['timestamp']}

    def trades(self, pair, **kwargs):
        if kwargs:
            q = kwargs
        else:
            q = {}
        r = self.query('GET', 'trades/%s' % pair, params=q).json()
        asks = []
        bids = []
        for order in r:
            order_to_list = [order['tid'], order['price'], order['amount'],
                             order['timestamp'], 'NA']
            order_to_list = [str(item) for item in order_to_list]

            if order['type'] == 'sell':
                asks.append(order_to_list)
            elif order['type'] == 'buy':
                bids.append(order_to_list)
            else:
                raise ValueError("Unknown value in 'type'! %s" % order)

            return {'asks': asks, 'bids': bids}

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
    uix.order_book('btcusd')
