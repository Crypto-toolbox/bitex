"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BitstampREST

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitstamp(BitstampREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bitstamp, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    def ticker(self, pair):
        return self.public_query('v2/ticker/%s/' % pair).json()

    def hourly_ticker(self, pair):
        return self.public_query('v2/ticker_hour/%s' % pair).json()

    def order_book(self, pair):
        return self.public_query('v2/order_book/%s' % pair).json()

    def trades(self, pair, **kwargs):
        return self.public_query('v2/transactions/%s' % pair, params=kwargs).json()

    def eurusd_rate(self):
        return self.public_query('eur_usd').json()


