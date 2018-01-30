"""Base class for formatters."""
# Import Built-ins
import datetime
from collections import namedtuple
from abc import abstractmethod, ABCMeta

# Import third-party
import requests


# pylint: disable=super-init-not-called
class APIResponse(requests.Response, metaclass=ABCMeta):
    """The base class that each formatter has to implement.

    It adds a `formatted` property, which returns a namedtuple with data
    converted from the json response.
    """

    def __init__(self, method, response_obj, *args, **kwargs):
        """Initialize the object."""
        if not isinstance(response_obj, requests.Response):
            raise TypeError("Response obj must be requests.Response instance, "
                            "not %s" % type(response_obj))
        self.response = response_obj
        self.method = method
        self.method_args = args
        self.method_kwargs = kwargs
        self.received_at_dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        self._cached_formatted = None

    def __getattr__(self, attr):
        """Use methods of the encapsulated object, otherwise use what's available in the wrapper."""
        try:
            return getattr(self.response, attr)
        except AttributeError:
            return getattr(self, attr)

    @property
    def received_at(self):
        """Return APIResponse timestamp as ISO formatted string."""
        return self.received_at_dt.isoformat()

    @property
    def formatted(self):
        """Return the formatted data, extracted from the json response."""
        if not self._cached_formatted:
            self._cached_formatted = getattr(self, self.method)
        return self._cached_formatted

    @abstractmethod
    def ticker(self, bid, ask, high, low, last, volume, ts):
        """Return namedtuple with given data."""
        ticker = namedtuple("Ticker", ("bid", "ask", "high", "low", "last", "volume", "timestamp"))
        return ticker(bid, ask, high, low, last, volume, ts)

    @abstractmethod
    def order_book(self, bids, asks, ts):
        """Return namedtuple with given data."""
        order_book = namedtuple("OrderBook", ("bids", "asks", "timestamp"))
        return order_book(bids, asks, ts)

    @abstractmethod
    def trades(self, trades, ts):
        """Return namedtuple with given data."""
        fmt_trades = namedtuple('Trades', ("trades", "timestamp"))
        return fmt_trades(trades, ts)

    @abstractmethod
    def bid(self, price, size, side, oid, otype, ts):
        """Return namedtuple with given data."""
        bid = namedtuple('Bid', ("price", "size", "side", "order_id", "order_type", "timestamp"))
        return bid(price, size, side, oid, otype, ts)

    @abstractmethod
    def ask(self, price, size, side, oid, otype, ts):
        """Return namedtuple with given data."""
        ask = namedtuple('Ask', ("price", "size", "side", "order_id", "order_type", "timestamp"))
        return ask(price, size, side, oid, otype, ts)

    @abstractmethod
    def order_status(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError

    @abstractmethod
    def open_orders(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError

    @abstractmethod
    def wallet(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError
