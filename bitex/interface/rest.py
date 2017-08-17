# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.utils import check_and_format_pair
from bitex.interface.base import Interface

# Init Logging Facilities
log = logging.getLogger(__name__)


class RESTInterface(Interface):
    def __init__(self, name, rest_api):
        super(RESTInterface, self).__init__(name=name, rest_api=rest_api)

    def _get_supported_pairs(self):
        return []

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        raise NotImplementedError

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        raise NotImplementedError

    def cancel_order(self, *order_ids, **kwargs):
        raise NotImplementedError

    def wallet(self, *args, **kwargs):
        raise NotImplementedError
