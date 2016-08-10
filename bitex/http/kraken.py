"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging
import requests

# Import Homebrew
from bitex.api.rest import KrakenREST
from bitex.http.client import Client


log = logging.getLogger(__name__)


class KrakenHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = KrakenREST(key, secret)
        if key_file:
            api.load_key(key_file)
        super(KrakenHTTP, self).__init__(api, 'Kraken')

    def order_book(self, pair, count=0):
        """
        Returns orderbook for passed asset pair.
        :param pair:
        :param count:
        :return:
        """
        q = {'pair': pair}
        if count:
            q['count'] = count

        return self.query('public/Depth', params=q)

    def server_time(self):
        """
        Returns the Kraken server time in unix
        :return: list
        """
        return self.query('public/Time')

    def ticker(self, pair):
        """
        Returns Ticker information for passed asset pairs.
        :param pairs:
        :return:
        """

        q = {'pair': pair}
        r = self.query('public/Ticker', params=q).json()

        return {'last': r['result'][pair]['c'][0],
                '24h Vol': r['result'][pair]['v'][1],
                'ask': r['result'][pair]['a'][0],
                'bid': r['result'][pair]['b'][0],
                'timestamp': r['result'][pair]['c'][0]}




    def trades(self, pair, since=None):
        """
        Returns trades for passed asset pair.
        :param pair:
        :param since:
        :return:
        """
        q = {'pair': pair}
        if since is not None:
            q['since'] = None

        return self.query('public/Trades', params=q)

    def balance(self, asset='ZUSD', aclass=None):
        """
        Returns user's account balance.
        :param asset: Base asset used to determine balance (default ZUSD)
        :param aclass: asset class - default is currency.
        :return: dict
        """
        q = {'asset': asset}
        if aclass is not None:
            q['aclass'] = aclass

        return self._api.query('private/TradeBalance', req_type='POST',
                               authenticate=True, params=q)

    def open_orders(self, trades=False, userref=None):
        """
        Returns user account's open orders.
        :param trades:
        :param userref:
        :return:
        """
        q = {}
        if trades:
            q['trades'] = trades

        if userref is not None:
            q['userref'] = userref

        return self.query('private/OpenOrders', req_type='POST',
                          authenticate=True, params=q)

    def add_order(self, pair, volume, price, order_type='limit', **kwargs):
        """
        Add an order for passed pair of passed ordertype and volume.
        :return:
        """
        q = {'pair': pair, 'ordertype': order_type, 'volume': volume,
             'price': price}

        if kwargs:
            q.update(kwargs)
        return self.query('private/AddOrder', req_type='POST',
                          authenticate=True, params=q)

    def cancel_order(self, txid):
        """
        Cancel an order by passed txid.
        :param txid:
        :return:
        """
        q = {'txid': txid}

        return self.query('CancelOrder', req_type='POST', authenticate=True,
                          params=q)

if __name__ == '__main__':
    test = KrakenHTTP()




