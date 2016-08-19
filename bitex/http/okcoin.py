"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging
import time

# Import Third-Party

# Import Homebrew
from bitex.api.rest import OKCoinREST

log = logging.getLogger(__name__)


class OKCoinHTTP(OKCoinREST):
    def __init__(self, key='', secret='', key_file=''):
        super(OKCoinHTTP, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def order_book(self, pair):
        q = {'pair': pair}
        r = self.query('GET', '/depth.do', params=q).json()
        t = time.time()
        asks = r['asks']
        bids = r['bids']
        for i in range(len(asks)):
            asks[i].append(t)
            asks[i] = [str(i) for i in asks[i]]
        for i in range(len(bids)):
            bids[i].append(t)
            bids[i] = [str(i) for i in bids[i]]
        return {'asks': asks, 'bids': bids}

    def ticker(self, pair):
        r = self.query('GET', '/ticker.do', params={'symbol': pair}).json()
        return {'last': r['ticker']['last'], '24h Vol': r['ticker']['vol'],
                'ask': r['ticker'] ['sell'], 'bid': r['ticker']['buy'],
                'timestamp': r['date']}

    def trades(self, pair):
        q = {'pair': pair}
        r = self.query('GET', '/trades.do', params=q).json()

        asks = []
        bids = []
        for trade in r:
            t = [str(trade['tid']), str(trade['price']), str(trade['amount']),
                 str(trade['date_ms']), 'NA']
            if trade['type'] == 'sell':
                asks.append(t)
            elif trade['type'] == 'buy':
                bids.append(t)
        return {'asks': asks, 'bids': bids}

if __name__ == '__main__':
    uix = OKCoinHTTP()
    print(uix.ticker('btc_usd').text)

