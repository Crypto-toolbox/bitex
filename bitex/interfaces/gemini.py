"""
https://docs.gemini.com/rest-api/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import GeminiREST
from bitex.utils import return_json

# Init Logging Facilities
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Gemini(GeminiREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Gemini, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)
        print(self.uri)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    @return_json
    def pairs(self):
        return self.public_query('symbols')

    @return_json
    def ticker(self, pair):
        return self.public_query('pubticker/%s' % pair)

    @return_json
    def order_book(self, pair, **kwargs):
        return self.public_query('book/%s' % pair, params=kwargs)

    @return_json
    def trades(self, pair, **kwargs):
        return self.public_query('trades/%s' % pair, params=kwargs)

    @return_json
    def auction(self, pair):
        return self.public_query('auction/%s' % pair)

    @return_json
    def auction_history(self, pair, **kwargs):
        return self.public_query('auction/%s/history' % pair, params=kwargs)





