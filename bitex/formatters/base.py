"""Base class for formatters."""

import requests
import datetime
from collections import namedtuple
from abc import abstractmethod, ABCMeta


class APIResponse(requests.Response, metaclass=ABCMeta):
    """The base class that each formatter has to implement.

    It adds a `formatted` property, which returns a namedtuple with data
    converted from the json response.
    """

    def __init__(self, method, response_obj, *args, **kwargs):
        self.response = response_obj
        self.method = method
        self.method_args = args
        self.method_kwargs = kwargs
        self.received_at_dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

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
        return getattr(self, self.method)

    @abstractmethod
    def ticker(self, bid, ask, high, low, last, volume, ts):
        """Return namedtuple with given data."""
        t = namedtuple("Ticker", ("bid", "ask", "high", "low", "last", "volume", "timestamp"))
        return t(bid, ask, high, low, last, volume, ts)

    @abstractmethod
    def order_book(self, bids, asks, ts):
        """Return namedtuple with given data."""
        ob = namedtuple("Order Book", ("bids", "asks", "timestamp"))
        return ob(bids, asks, ts)

    @abstractmethod
    def trades(self, trades, ts):
        """Return namedtuple with given data."""
        t = namedtuple('Trades', ("trades", "timestamp"))
        return t(trades, ts)

    @abstractmethod
    def bid(self, price, size, side, oid, otype, ts):
        """Return namedtuple with given data."""
        t = namedtuple('Bid', ("price", "size", "side", "order_id", "order_type", "timestamp"))
        return t(price, size, side, oid, otype, ts)

    @abstractmethod
    def ask(self, price, size, side, oid, otype, ts):
        """Return namedtuple with given data."""
        t = namedtuple('Ask', ("price", "size", "side", "order_id", "order_type", "timestamp"))
        return t(price, size, side, oid, otype, ts)

    @abstractmethod
    def order_status(self, *args):
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, *args):
        raise NotImplementedError

    @abstractmethod
    def open_orders(self, *args):
        raise NotImplementedError

    @abstractmethod
    def wallet(self, *args):
        raise NotImplementedError

