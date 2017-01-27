"""
https://docs.gemini.com/rest-api/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import GeminiREST
from bitex.utils import return_json
from bitex.formatters.gemini import GmniFormatter as fmt

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

    def private_query(self, endpoint, method_verb='POST', **kwargs):
        return self.query(method_verb, endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """

    @return_json(fmt.ticker)
    def ticker(self, pair, **kwargs):
        return self.public_query('pubticker/%s' % pair, params=kwargs)

    @return_json(fmt.order_book)
    def order_book(self, pair, **kwargs):
        return self.public_query('book/%s' % pair, params=kwargs)

    @return_json(fmt.trades)
    def trades(self, pair, **kwargs):
        return self.public_query('trades/%s' % pair, params=kwargs)

    @return_json(fmt.order)
    def bid(self, pair, price, size, **kwargs):
        q = {'symbol': pair, 'amount': size, 'price': price, 'side': 'buy'}
        q.update(kwargs)
        return self.private_query('order/new', params=q)

    @return_json(fmt.order)
    def ask(self, pair, price, size, **kwargs):
        q = {'symbol': pair, 'amount': size, 'price': price, 'side': 'sell'}
        q.update(kwargs)
        return self.private_query('order/new', params=q)

    @return_json(fmt.cancel)
    def cancel_order(self, order_id, **kwargs):
        q = {'order_id': order_id}
        q.update(kwargs)
        return self.private_query('order/cancel', params=q)

    @return_json(fmt.order_status)
    def order(self, order_id, **kwargs):
        q = {'order_id': order_id}
        q.update(kwargs)
        return self.private_query('order/status', params=q)

    @return_json(fmt.balance)
    def balance(self, **kwargs):
        return self.private_query('balances', params=kwargs)

    @return_json(fmt.withdraw)
    def withdraw(self, amount, tar_addr, **kwargs):
        raise NotImplementedError()

    @return_json(fmt.deposit)
    def deposit_address(self, **kwargs):
        raise NotImplementedError()

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def pairs(self):
        return self.public_query('symbols')

    @return_json(None)
    def auction(self, pair):
        return self.public_query('auction/%s' % pair)

    @return_json(None)
    def auction_history(self, pair, **kwargs):
        return self.public_query('auction/%s/history' % pair, params=kwargs)
