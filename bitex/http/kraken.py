"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging
import requests

# Import Homebrew
from bitex.api.rest import KrakenREST


log = logging.getLogger(__name__)


class KrakenHTTP(KrakenREST):
    def __init__(self, key='', secret='', key_file=''):

        super(KrakenHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair, **kwargs):
        """
        Returns orderbook for passed asset pair.
        :param pair:
        :param count:
        :return:
        """
        q = {'pair': pair}
        q.update(kwargs)

        r = self.query('GET', 'public/Depth', params=q).json()['result']
        r = r[list(r.keys())[0]]
        for i in range(len(r['asks'])):
            r['asks'][i] = [str(i) for i in r['asks'][i]]

        for i in range(len(r['bids'])):
            r['bids'][i] = [str(i) for i in r['bids'][i]]

        return {'asks': r['asks'], 'bids': r['bids']}

    def ticker(self, pair):
        """
        Returns Ticker information for passed asset pairs.
        :param pairs:
        :return:
        """

        q = {'pair': pair}
        r = self.query('GET', 'public/Ticker', params=q).json()

        return {'last': r['result'][pair]['c'][0],
                '24h Vol': r['result'][pair]['v'][1],
                'ask': r['result'][pair]['a'][0],
                'bid': r['result'][pair]['b'][0],
                'timestamp': r['result'][pair]['c'][0]}

    def trades(self, pair, **kwargs):
        """
        Returns trades for passed asset pair.
        :param pair:
        :param since:
        :return:
        """
        q = {'pair': pair}
        q.update(kwargs)

        r = self.query('GET', 'public/Trades', params=q).json()['result']
        r.pop('last')
        r = r[list(r.keys())[0]]
        data = {'asks': [], 'bids': []}
        for quote in r:
            q = [str(i) for i in ( ['NA'] + quote[:3] + [quote[4]])]
            if quote[3] == 'b':
                data['bids'].append(q)
            else:
                data['asks'].append(q)
        return data

    def balance(self, **kwargs):
        """
        Returns user's account balance.
        :param asset: Base asset used to determine balance (default ZUSD)
        :param aclass: asset class - default is currency.
        :return: dict
        """
        q = kwargs

        resp = self.query('POST', 'private/TradeBalance', req_type='POST',
                          authenticate=True, params=q)
        return resp

    def orders(self, trades=False, userref=None):
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

        return self.query('POST', 'private/OpenOrders', req_type='POST',
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
        return self.query('POST', 'private/AddOrder', req_type='POST',
                          authenticate=True, params=q)

    def cancel_order(self, txid):
        """
        Cancel an order by passed txid.
        :param txid:
        :return:
        """
        q = {'txid': txid}

        return self.query('POST', 'CancelOrder', req_type='POST', authenticate=True,
                          params=q)

if __name__ == '__main__':
    test = KrakenHTTP(key_file='../../../keys/kraken.key')
    r = test.ticker('XXBTZUSD')
    print(r.request.body)



