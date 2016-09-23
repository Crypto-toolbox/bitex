"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BitfinexREST

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitfinex(BitfinexREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bitfinex, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def ticker(self, pair):
        return self.public_query('pubticker/%s' % pair).json()

    def statistics(self, pair):
        return self.public_query('stats/%s' % pair).json()

    def funding_book(self, currency, **kwargs):
        return self.public_query('lendbook/%s' % currency, params=kwargs).json()

    def order_book(self, pair, **kwargs):
        return self.public_query('book/%s' % pair, params=kwargs).json()

    def trades(self, pair, **kwargs):
        return self.public_query('trades/%s' % pair, params=kwargs)

    def lends(self, currency, **kwargs):
        return self.public_query('lends/%s' % currency, params=kwargs)

    def pairs(self, details=False):
        if details:
            return self.public_query('symbols_details')
        else:
            return self.public_query('symbols')




print(Bitfinex().ticker('btcusd'))
print(Bitfinex().funding_book('btc', limit_bids=1, limit_asks=1))