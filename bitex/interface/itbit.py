"""ItBit Interface class."""
# pylint: disable=abstract-method
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.itbit import ITbitREST
from bitex.interface.rest import RESTInterface
from bitex.formatters import ItBitFormattedResponse
from bitex.utils import format_with, check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class ItBit(RESTInterface):
    """itBit Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(ItBit, self).__init__('ItBit', ITbitREST(**api_kwargs))

    def _get_supported_pairs(self):
        return []

    # Public Endpoints
    @check_and_format_pair
    @format_with(ItBitFormattedResponse)
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
    @format_with(ItBitFormattedResponse)
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
    @format_with(ItBitFormattedResponse)
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
    @format_with(ItBitFormattedResponse)
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
    @format_with(ItBitFormattedResponse)
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

    @format_with(ItBitFormattedResponse)
    def order_status(self, order_id, *args, **kwargs):
        """
        Return the status of an order with the given id.

        :param order_id: Order ID of the order you'd like to have a status for.
        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(ItBitFormattedResponse)
    def open_orders(self, *args, **kwargs):
        """
        Return all open orders.

        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(ItBitFormattedResponse)
    def cancel_order(self, *order_ids, **kwargs):
        """
        Cancel the order(s) with the given id(s).

        :param order_ids: variable amount of order IDs to cancel.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError

    @format_with(ItBitFormattedResponse)
    def wallet(self, *args, **kwargs):
        """
        Return the wallet of this account.

        :param args: additional arguments.
        :param kwargs: additional kwargs, passed to requests.Requests() as 'param' kwarg.
        :return: :class:`requests.Response()` object.
        """
        raise NotImplementedError