"""
https://c-cex.com/?id=api
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import CCEXRest
from bitex.utils import return_json

# Init Logging Facilities
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class CCEX(CCEXRest):
    def __init__(self, key='', secret='', key_file=''):
        super(CCEX, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)
        print(self.uri)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json
    def ticker(self, pair):
        return self.public_query('%s.json' % pair)

    @return_json
    def pairs(self, names_only=True):
        if names_only:
            return self.public_query('api_pub.html?a=getmarkets')
        else:
            return self.public_query('pairs.json')

    @return_json
    def prices(self):
        return self.public_query('prices.json')

    @return_json
    def coin_names(self):
        return self.public_query('coinnames.json')

    @return_json
    def volume(self, pair):
        return self.public_query('volume_%s.json' % pair)

    @return_json
    def trades(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('api_pub.html?a=getmarkethistory' % pair,
                                 params=q)

    @return_json
    def statistics(self, all=True):
        if all:
            return self.public_query('api_pub.html?a=getmarketsummaries')

    @return_json
    def order_book(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('api_pub.html?a=getorderbook', params=q)

    @return_json
    def balance_distribution(self, currency):
        return self.public_query('api_pub.html?a=getbalancedistribution',
                                 params={'currencyname': currency})


