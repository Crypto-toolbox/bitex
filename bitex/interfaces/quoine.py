"""
https://www.bitstamp.net/api/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import QuoineREST
from bitex.utils import return_json
from bitex.formatters.quoine import QoinFormatter as fmt

# Init Logging Facilities
log = logging.getLogger(__name__)


class Quoine(QuoineREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Quoine, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

        self.pairs = {d['currency_pair_code']: d['id'] for d in self.public_query('products')}

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, method='POST',**kwargs):
        return self.query(method, endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """

    @return_json(fmt.ticker)
    def ticker(self, pair):
        pair = self.pairs[pair]
        return self.public_query('products/%s' % pair)

    @return_json(fmt.order_book)
    def order_book(self, pair, **kwargs):
        pair = self.pairs[pair]
        return self.public_query('products/%s/price_levels' % pair, params=kwargs)

    @return_json(fmt.trades)
    def trades(self, pair, **kwargs):
        q = {'currency_pair_code': pair}
        q.update(kwargs)
        return self.public_query('executions/', params=q)

    @return_json(fmt.order)
    def bid(self, pair, price, size, **kwargs):
        q = {'quantity': size, 'price': price, 'order_type': 'limit',
             'product_id': self.pairs[pair], 'side': 'buy'}
        q.update(kwargs)
        return self.private_query('orders/' % pair, params=q)

    @return_json(fmt.order)
    def ask(self, pair, price, size, **kwargs):
        q = {'quantity': size, 'price': price, 'order_type': 'limit',
             'product_id': self.pairs[pair], 'side': 'sell'}
        q.update(kwargs)
        return self.private_query('orders/' % pair, params=q)

    @return_json(fmt.cancel)
    def cancel_order(self, order_id, **kwargs):
        return self.private_query('cancel_order/%s/cancel' % order_id,
                                  method='PUT')

    @return_json(fmt.order_status)
    def order(self, order_id, **kwargs):
        q = {'id': order_id}
        q.update(kwargs)
        return self.private_query('orders/', params=q, method='GET')

    @return_json(fmt.balance)
    def balance(self, **kwargs):
        return self.private_query('/accounts/balance/', method='GET')

    @return_json(fmt.withdraw)
    def withdraw(self, amount, tar_addr, **kwargs):
        raise NotImplementedError()

    @return_json(fmt.deposit)
    def deposit_address(self, **kwargs):
        raise NotImplementedError()

    """
    Exchange Specific Methods
    """

