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

    """
    BitEx Standardized Methods
    """

    @return_json(None)
    def ticker(self, pair):
        return self.public_query('%s.json' % pair)

    @return_json(None)
    def order_book(self, pair, type='both', **kwargs):
        q = {'market': pair, 'type': type}
        q.update(kwargs)
        return self.public_query('api_pub.html?a=getorderbook', params=q)

    @return_json(None)
    def trades(self, pair, **kwargs):
        q = {'market': pair}
        q.update(kwargs)
        return self.public_query('api_pub.html?a=getmarkethistory',
                                 params=q)

    @return_json(None)
    def bid(self, pair, price, amount, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def ask(self, pair, price, amount, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def cancel_order(self, order_id, all=False, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def order(self, order_id, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def balance(self, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def withdraw(self, _type, source_wallet, amount, tar_addr, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def deposit_address(self, **kwargs):
        raise NotImplementedError()

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def pairs(self, names_only=True):
        if names_only:
            return self.public_query('api_pub.html?a=getmarkets')
        else:
            return self.public_query('pairs.json')

    @return_json(None)
    def prices(self):
        return self.public_query('prices.json')

    @return_json(None)
    def coin_names(self):
        return self.public_query('coinnames.json')

    @return_json(None)
    def volume(self, pair):
        return self.public_query('volume_%s.json' % pair)



    @return_json(None)
    def statistics(self, all=True):
        if all:
            return self.public_query('api_pub.html?a=getmarketsummaries')


    @return_json(None)
    def balance_distribution(self, currency):
        return self.public_query('api_pub.html?a=getbalancedistribution',
                                 params={'currencyname': currency})

