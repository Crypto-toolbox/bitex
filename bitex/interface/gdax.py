"""GDAX Interface class."""
# pylint: disable=abstract-method
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.gdax import GDAXREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair, format_with
from bitex.formatters.gdax import GDAXFormattedResponse

# Init Logging Facilities
log = logging.getLogger(__name__)


class GDAX(RESTInterface):
    """GDAX Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(GDAX, self).__init__('GDAX', GDAXREST(**api_kwargs))

    def _get_supported_pairs(self):
        return []

    # Public Endpoints
    @check_and_format_pair
    @format_with(GDAXFormattedResponse)
    def ticker(self, pair, *args, **kwargs):
        """
        Return the ticker for the given pair.

        :param pair: Str, pair to request data for.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @check_and_format_pair
    @format_with(GDAXFormattedResponse)
    def order_book(self, pair, *args, **kwargs):
        """
        Return the order book for the given pair.

        :param pair: Str, pair to request data for.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @check_and_format_pair
    @format_with(GDAXFormattedResponse)
    def trades(self, pair, *args, **kwargs):
        """
        Return the trades for the given pair.

        :param pair: Str, pair to request data for.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    # Private Endpoints
    @check_and_format_pair
    @format_with(GDAXFormattedResponse)
    def ask(self, pair, price, size, *args, **kwargs):
        """
        Place an ask order.

        :param pair: Str, pair to post order for.
        :param price: Float or str, price you'd like to ask.
        :param size: Float or str, amount of currency you'd like to sell.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @check_and_format_pair
    @format_with(GDAXFormattedResponse)
    def bid(self, pair, price, size, *args, **kwargs):
        """
        Place a bid order.

        :param pair: Str, pair to post order for.
        :param price: Float or str, price you'd like to bid.
        :param size: Float or str, amount of currency you'd like to buy.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(GDAXFormattedResponse)
    def order_status(self, order_id, *args, **kwargs):
        """
        Return the status of an order with the given id.

        :param order_id: Order ID of the order you'd like to have a status for.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(GDAXFormattedResponse)
    def open_orders(self, *args, **kwargs):
        """
        Return all open orders.

        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(GDAXFormattedResponse)
    def cancel_order(self, *order_ids, **kwargs):
        """
        Cancel the order(s) with the given id(s).

        :param order_ids: variable amount of order IDs to cancel.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(GDAXFormattedResponse)
    def wallet(self, *args, **kwargs):
        """
        Return the wallet of this account.

        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError
