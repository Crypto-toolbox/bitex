"""
https://www.therocktrading.com/pages/api
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import RockTradingREST
from bitex.utils import return_json

# Init Logging Facilities
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class RockTradingLtd(RockTradingREST):
    def __init__(self, key='', secret='', key_file=''):
        super(RockTradingLtd, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)
        print(self.uri)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, method='GET', **kwargs):
        return self.query(method, endpoint, authenticate=True, **kwargs)

    @return_json(None)
    def ticker(self, pair):
        return self.public_query('ticker/%s' % pair)

    @return_json(None)
    def tickers(self, currency=None):
        if currency:
            return self.public_query('funds/%s/ticker' % currency)
        else:
            return self.public_query('tickers')

    @return_json(None)
    def order_book(self, pair):
        return self.public_query('funds/%s/orderbook' % pair)

    @return_json(None)
    def trades(self, pair):
        return self.public_query('funds/%s/trades' % pair)

    @return_json(None)
    def balance(self):
        return self.private_query('balances')

    @return_json(None)
    def cancel_order(self, id, market):
        return self.private_query('funds/%s/orders/%s' % (market, id), method='DELETE')

    def _place_order(self, side, pair, price, size, **kwargs):
        q = {'fund_id': pair, 'side': side, 'amount': size, 'price': price}
        q.update(kwargs)
        return self.private_query('funds/%s/orders' % pair, method='POST', params=q)

    @return_json(None)
    def bid(self, pair, price, size, **kwargs):
        return self._place_order('buy', pair, price, size)

    @return_json
    def ask(self, *, pair, price, size, **kwargs):
        return self._place_order('sell', pair, price, size, **kwargs)
