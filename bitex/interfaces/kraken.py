"""
https:/kraken.com/help/api
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import KrakenREST
from bitex.utils import return_json
from bitex.formatters.kraken import cancel, trade, order_book
# Init Logging Facilities
log = logging.getLogger(__name__)


class Kraken(KrakenREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Kraken, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def make_params(self, *pairs, **kwargs):
        q = {'pair': ','.join(pairs)}
        q.update(kwargs)
        return q

    def public_query(self, endpoint, **kwargs):
        path = 'public/' + endpoint
        return self.query('GET', path, **kwargs)

    def private_query(self, endpoint, **kwargs):
        path = 'private/' + endpoint
        return self.query('POST', path, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """

    @return_json(None)
    def ticker(self, *pairs):
        q = self.make_params(*pairs)
        return self.public_query('Ticker', params=q)

    @return_json(order_book)
    def order_book(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('Depth', params=q)

    @return_json(None)
    def trades(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('Trades', params=q)

    def _add_order(self, pair, side, price, amount, **kwargs):
        q = {'pair': pair, 'type': side, 'price': price,
             'ordertype': 'limit', 'volume': amount,
             'trading_agreement': 'agree'}
        q.update(kwargs)
        return self.private_query('AddOrder', params=q)

    @return_json(trade)
    def bid(self, pair, price, amount, **kwargs):
        return self._add_order(pair, 'buy', price, amount, **kwargs)

    @return_json(trade)
    def ask(self, pair, price, amount, **kwargs):
        return self._add_order(pair, 'sell', price, amount, **kwargs)

    @return_json(cancel)
    def cancel_order(self, order_id, **kwargs):
        q = {'txid': order_id}
        q.update(kwargs)
        return self.private_query('CancelOrder', params=q)

    @return_json(None)
    def order_info(self, *txids, **kwargs):
        if len(txids) > 1:
            q = {'txid': txids}
        elif txids:
            txid, *_ = txids
            q = {'txid': txid}
        else:
            q = {}
        q.update(kwargs)
        return self.private_query('QueryOrders', params=q)

    @return_json(None)
    def balance(self, **kwargs):
        return self.private_query('Balance')

    @return_json(None)
    def withdraw(self, amount, tar_addr, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def deposit_address(self, **kwargs):
        raise NotImplementedError()

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def time(self):
        return self.public_query('Time')

    @return_json(None)
    def assets(self, **kwargs):
        return self.public_query('Assets', params=kwargs)

    @return_json(None)
    def pairs(self, **kwargs):
        return self.public_query('AssetPairs', params=kwargs)

    @return_json(None)
    def ohlc(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('OHLC', params=q)

    @return_json(None)
    def spread(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('Spread', params=q)

    @return_json(None)
    def orders(self, **kwargs):
        q = kwargs
        return self.private_query('OpenOrders', params=q)

    @return_json(None)
    def closed_orders(self, **kwargs):
        q = kwargs
        return self.private_query('ClosedOrders', params=q)

    @return_json(None)
    def trade_history(self, **kwargs):
        q = kwargs
        return self.private_query('TradesHistory', params=q)

    @return_json(None)
    def fees(self, pair=None):
        q = {'fee-info': True}

        if pair:
            q['pair'] = pair

        return self.private_query('TradeVolume', params=q)
