"""
https://docs.gdax.com/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import GDAXRest
from bitex.utils import return_json

# Init Logging Facilities
log = logging.getLogger(__name__)


class GDAX(GDAXRest):
    def __init__(self, key='', secret='', key_file=''):
        super(GDAX, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json
    def time(self):
        return self.public_query('time')

    @return_json(None)
    def currencies(self):
        return self.public_query('currencies')

    @return_json(None)
    def pairs(self):
        return self.public_query('products')

    @return_json(None)
    def order_book(self, pair, **kwargs):
        return self.public_query('products/%s/book' % pair, params=kwargs)

    @return_json(None)
    def ticker(self, pair, **kwargs):
        return self.public_query('products/%s/ticker' % pair, params=kwargs)

    @return_json(None)
    def trades(self, pair, **kwargs):
        return self.public_query('products/%s/trades' % pair, params=kwargs)

    @return_json(None)
    def ohlc(self, pair, **kwargs):
        return self.public_query('products/%s/candles' % pair, params=kwargs)

    @return_json(None)
    def stats(self, pair, **kwargs):
        return self.public_query('products/%s/stats' % pair, params=kwargs)


