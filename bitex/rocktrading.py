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

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json
    def ticker(self, pair):
        return self.public_query('ticker/%s' % pair)

    @return_json
    def tickers(self, currency=None):
        if currency:
            return self.public_query('tickers/%s' % currency)
        else:
            return self.public_query('tickers')

    @return_json
    def order_book(self, pair):
        return self.public_query('orderbook/%s' % pair)

    @return_json
    def trades(self, pair):
        return self.public_query('trades/%s' % pair)




