"""FormattedResponse Class for Standardized methods of the QuadrigaCX Interface class."""
# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class QuadrigaCXFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        bid = data["bidPrice"]
        ask = data["askPrice"]
        high = data["highPrice"]
        low = data["lowPrice"]
        last = data["lastPrice"]
        volume = data["volume"]
        timestamp = datetime.utcnow()
        return super(QuadrigaCXFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                               timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def trades(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def bid(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def ask(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def order_status(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def cancel_order(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def open_orders(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def wallet(self):
        """Return namedtuple with given data."""
        raise NotImplementedError