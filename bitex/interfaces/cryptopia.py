"""
https://www.cryptopia.co.nz/Forum/Category/45
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import CryptopiaREST
from bitex.utils import return_json

# Init Logging Facilities
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Cryptopia(CryptopiaREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Cryptopia, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)
        print(self.uri)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json(None)
    def currencies(self):
        return self.public_query('GetCurrency')

    @return_json(None)
    def pairs(self):
        return self.public_query('GetTradePairs')

    @return_json(None)
    def markets(self, **kwargs):
        endpoint = 'GetMarkets'
        for k in kwargs:
            endpoint += '/' + kwargs[k]
        return self.public_query(endpoint, params=kwargs)

    @return_json(None)
    def ticker(self, pair, **kwargs):
        endpoint = 'GetMarket/%s' % pair
        for k in kwargs:
            endpoint += '/' + kwargs[k]
        return self.public_query(endpoint, params=kwargs)

    @return_json(None)
    def trades(self, pair, **kwargs):
        endpoint = 'GetMarkets/%s' % pair
        for k in kwargs:
            endpoint += '/' + kwargs[k]
        return self.public_query(endpoint, params=kwargs)

    @return_json(None)
    def order_book(self, pair, **kwargs):
        endpoint = 'GetMarketOrders/%s' % pair
        for k in kwargs:
            endpoint += '/' + kwargs[k]
        return self.public_query(endpoint, params=kwargs)
