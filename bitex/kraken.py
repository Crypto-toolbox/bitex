"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import KrakenREST
from bitex.utils import return_json
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

    @return_json
    def time(self):
        return self.public_query('Time')

    @return_json
    def assets(self, **kwargs):
        return self.public_query('Assets', params=kwargs)

    @return_json
    def pairs(self, **kwargs):
        return self.public_query('AssetPairs', params=kwargs)

    @return_json
    def ticker(self, *pairs):
        q = self.make_params(*pairs)
        return self.public_query('Ticker', params=q)

    @return_json
    def ohlc(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('OHLC', params=q)

    @return_json
    def order_book(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('Depth', params=q)

    @return_json
    def trades(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('Trades', params=q)

    @return_json
    def spread(self, pair, **kwargs):
        q = self.make_params(pair, **kwargs)
        return self.public_query('Spread', params=q)


print(Kraken().order_book('XXBTXLTC'))