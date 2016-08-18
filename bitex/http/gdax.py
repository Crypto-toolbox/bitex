"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging
import time
import datetime

# Import Third-Party
from bitex.api.rest import GDAXRest

# Import Homebrew

log = logging.getLogger(__name__)


class GdaxHTTP(GDAXRest):
    def __init__(self, passphrase='', key='', secret='', key_file=''):

        super(GdaxHTTP, self).__init__(passphrase, key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair, level=3, **kwargs):
        q = {'level': level}
        q.update(kwargs)
        r = self.query('GET', 'products/%s/book' % pair, params=q).json()
        t = time.time()
        for i in range(len(r['asks'])):
            r['asks'][i] = r['asks'][i][:2]
            r['asks'][i].append(str(t))

        for i in range(len(r['bids'])):
            r['bids'][i] = r['bids'][i][:2]
            r['bids'][i].append(str(t))
        r.pop('sequence')
        return r

    def ticker(self, pair):
        r = self.query('GET', 'products/%s/ticker' % pair).json()
        t = datetime.datetime.strptime(r['time'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%s')

        return {'last': r['price'], '24h Vol': r['volume'], 'ask': r['ask'],
                'bid': r['bid'], 'timestamp': t}

    def trades(self, pair):
        r = self.query('GET', '/products/%s/trades' % pair).json()
        asks = []
        bids = []
        for order in r:
            t = datetime.datetime.strptime(order['time'],
                                           '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%s')
            to_list = [str(order['trade_id']), order['price'], order['size'], t,
                       'NA']
            if order['side'] == 'sell':
                asks.append(to_list)
            elif order['side'] == 'buy':
                bids.append(to_list)
            else:
                raise ValueError(order)
        return {'asks': asks, 'bids': bids}

    def accounts(self):
        return self.query('GET', 'accounts', authenticate=True)


if __name__ == '__main__':
    uix = GdaxHTTP()
    print(uix.ticker('BTC-USD'))

