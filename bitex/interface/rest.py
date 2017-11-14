"""REST Interface base class."""
# Import Built-Ins
import logging

# Import Homebrew
from bitex.utils import check_and_format_pair
from bitex.interface.base import Interface

# Init Logging Facilities
log = logging.getLogger(__name__)


class RESTInterface(Interface):
    """REST Interface base class."""

    def __init__(self, name, rest_api):
        """Initialize class instance."""
        super(RESTInterface, self).__init__(name=name, rest_api=rest_api)

    def _get_supported_pairs(self):
        return []

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        raise NotImplementedError

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        raise NotImplementedError

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        raise NotImplementedError

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask order."""
        raise NotImplementedError

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        """Return the status of an order with the given id."""
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        """Return all open orders."""
        raise NotImplementedError

    def cancel_order(self, *order_ids, **kwargs):
        """Cancel the order(s) with the given id(s)."""
        raise NotImplementedError

    def wallet(self, *args, **kwargs):
        """Return the wallet of this account."""
        raise NotImplementedError
