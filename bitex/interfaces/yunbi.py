"""
https://yunbi.com/documents/api/guide
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import YunbiREST
from bitex.utils import return_json

# Init Logging Facilities
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Yunbi(YunbiREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Yunbi, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint + '.json', **kwargs)

    def private_query(self, endpoint, method_verb='POST', **kwargs):
        return self.query(method_verb, endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """

    @return_json(None)
    def ticker(self, pair=None):
        if pair:
            return self.public_query('tickers/%s' % pair)
        else:
            return self.public_query('tickers')

    @return_json(None)
    def order_book(self, pair, **kwargs):
        q = {'market': pair}
        q.update(kwargs)
        return self.public_query('order_book', params=q)

    @return_json(None)
    def trades(self, pair, **kwargs):
        q = {'market': pair}
        q.update(kwargs)
        return self.public_query('trades', params=q)

    @return_json(None)
    def bid(self, pair, price, size, **kwargs):
        q = {'market': pair, 'side': 'buy', 'volume': size, 'price': price}
        q.update(kwargs)
        return self.private_query('orders.json', params=q)

    @return_json(None)
    def ask(self, pair, price, size, **kwargs):
        q = {'market': pair, 'side': 'sell', 'volume': size, 'price': price}
        q.update(kwargs)
        return self.private_query('orders.json', params=q)

    @return_json(None)
    def cancel_order(self, order_id, **kwargs):
        q = {'id': order_id}
        q.update(kwargs)
        return self.private_query('delete.json', params=q)

    @return_json(None)
    def order(self, order_id, **kwargs):
        q = {'id': order_id}
        q.update(kwargs)
        return self.private_query('delete.json', method_verb='GET', params=q)

    @return_json(None)
    def balance(self, **kwargs):
        return self.private_query('members/me.json', params=kwargs)

    @return_json(None)
    def withdraw(self, _type, source_wallet, amount, tar_addr, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def deposit_address(self, **kwargs):
        return self.private_query('deposit_addres.json', method_verb='GET',
                                  params=kwargs)

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def pairs(self):
        return self.public_query('symbols')

    @return_json(None)
    def ohlc(self, pair, **kwargs):
        q = {'market': pair}
        q.update(kwargs)
        return self.public_query('k', params=q)

    @return_json(None)
    def auction(self, pair):
        return self.public_query('auction/%s' % pair)

    @return_json(None)
    def auction_history(self, pair, **kwargs):
        return self.public_query('auction/%s/history' % pair, params=kwargs)



