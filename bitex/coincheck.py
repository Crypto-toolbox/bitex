"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import CoincheckREST
from bitex.utils import return_json

# Init Logging Facilities
log = logging.getLogger(__name__)


class Coincheck(CoincheckREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Coincheck, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json
    def ticker(self, pair):
        return self.public_query('ticker', params={'pair': pair})

    @return_json
    def trades(self, pair):
        return self.public_query('trades', params={'pair': pair})

    @return_json
    def order_book(self, pair):
        return self.public_query('order_book', params={'pair': pair})


