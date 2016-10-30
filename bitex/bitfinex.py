"""
http://docs.bitfinex.com/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BitfinexREST
from bitex.utils import return_json
# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitfinex(BitfinexREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bitfinex, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json
    def ticker(self, pair):
        return self.public_query('pubticker/%s' % pair)

    @return_json
    def statistics(self, pair):
        return self.public_query('stats/%s' % pair)

    @return_json
    def funding_book(self, currency, **kwargs):
        return self.public_query('lendbook/%s' % currency, params=kwargs)

    @return_json
    def order_book(self, pair, **kwargs):
        return self.public_query('book/%s' % pair, params=kwargs)

    @return_json
    def trades(self, pair, **kwargs):
        return self.public_query('trades/%s' % pair, params=kwargs)

    @return_json
    def lends(self, currency, **kwargs):
        return self.public_query('lends/%s' % currency, params=kwargs)

    @return_json
    def pairs(self, details=False):
        if details:
            return self.public_query('symbols_details')
        else:
            return self.public_query('symbols')
