"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import BitstampREST

log = logging.getLogger(__name__)


class BitstampHTTP(BitstampREST):
    def __init__(self, key='', secret='', user_id='', key_file=''):

        super(BitstampHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair, count=0):
        q = {'pair': pair}
        if count:
            q['count'] = count

        resp = self.query('GET', 'v2/order_book/%s/' % pair, params=q)

        ts = resp.json()['timestamp']
        asks = resp.json()['asks']
        bids = resp.json()['bids']
        for order_index in range(len(asks)):
            asks[order_index].append(ts)
            asks[order_index] = [str(i) for i in asks[order_index]]

        for order_index in range(len(bids)):
            bids[order_index].append(ts)
            bids[order_index] = [str(i) for i in bids[order_index]]

        return {'asks': asks, 'bids': bids}

    def ticker(self, pair):
        r = self.query('GET', 'v2/ticker/%s/' % pair).json()
        return {'last': r['last'], '24h Vol': r['volume'], 'ask': r['ask'],
                'bid': r['bid'], 'timestamp': r['timestamp']}

    def trades(self, pair, t='hour'):
        r = self.query('GET', 'v2/transactions/%s/' % pair, params={'time': t}).json()
        asks = []
        bids = []

        for order in r:
            book_side = order['type']
            order = [order['tid'], order['price'], order['amount'], order['date'], 'NA']
            if book_side == '1':  # ask
                asks.append(order)
            elif book_side == '0':  # bid
                bids.append(order)
            else:
                print(book_side)
                raise ValueError("something didnt work here.")
        return {'asks': asks, 'bids': bids}

    def balance(self, **kwargs):
        """
        Returns the balance of the exchange account's wallets.
        :param kwargs:
        :return:
        """
        return self.query('POST', 'v2/balance/', authenticate=True)

    def orders(self, *args, **kwargs):
        """
        Return open orders.
        :param pair:
        :param kwargs:
        :return:
        """
        return self.query('POST', 'v2/open_orders/%s/' % pair,
                          authenticate=True)

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
    print(uix.order_book('btcusd'))
    print(uix.trades('btcusd'))
    print(uix.ticker('btcusd'))


