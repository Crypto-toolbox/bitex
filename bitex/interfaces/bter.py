"""
https://bter.com/api
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BterREST
from bitex.utils import return_api_response
from bitex.formatters.bter import BterFormatter as fmt

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bter(BterREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bter, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    """
    BitEx Standardized Methods
    """

    @return_api_response(fmt.order_book)
    def order_book(self, pair, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.ticker)
    def ticker(self, pair, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.trades)
    def trades(self, pair, **kwargs):
        raise NotImplementedError

    def _place_order(self, pair, amount, price, side, replace, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.order)
    def bid(self, pair, price, amount, replace=False, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.order)
    def ask(self, pair, price, amount, replace=False, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.cancel)
    def cancel_order(self, order_id, all=False, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.order_status)
    def order(self, order_id, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.balance)
    def balance(self, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.withdraw)
    def withdraw(self, amount, tar_addr, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.deposit)
    def deposit_address(self, **kwargs):
        raise NotImplementedError