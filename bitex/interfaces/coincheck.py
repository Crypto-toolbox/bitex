"""
https://coincheck.com/documents/exchange/api
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

    """
    BitEx Standardized Methods
    """

    @return_json(None)
    def ticker(self, pair):
        return self.public_query('ticker', params={'pair': pair})

    @return_json(None)
    def trades(self, pair):
        return self.public_query('trades', params={'pair': pair})

    @return_json(None)
    def order_book(self, pair):
        return self.public_query('order_books', params={'pair': pair})

    @return_json(None)
    def bid(self, pair, price, size, **kwargs):
        q = {'rate': price, 'amount': size, 'pair': pair,
             'order_type': 'buy'}
        q.update(kwargs)
        return self.private_query('orders', params=q)

    @return_json(None)
    def ask(self, pair, price, size, **kwargs):
        q = {'rate': price, 'amount': size, 'pair': pair,
             'order_type': 'sell'}
        q.update(kwargs)
        return self.private_query('orders', params=q)

    @return_json(None)
    def cancel_order(self, order_id, **kwargs):
        return self.private_query('exchange/orders/%s' % order_id, params=kwargs)

    @return_json(None)
    def order(self, order_id, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def balance(self, **kwargs):
        return self.private_query('accounts/balance')

    @return_json(None)
    def withdraw(self, amount, tar_addr, **kwargs):
        q = {'address': tar_addr, 'amount': amount}
        q.update(kwargs)
        return self.private_query('send_money', params=q)

    @return_json(None)
    def deposit_address(self, **kwargs):
        raise NotImplementedError()

    """
    Exchange Specific Methods
    """

