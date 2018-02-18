"""FormattedResponse Class for Standardized methods of the OKCoin Interface class."""
# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class OKCoinFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        bid = data["ticker"]["buy"]
        ask = data["ticker"]["sell"]
        high = data["ticker"]["high"]
        low = data["ticker"]["low"]
        last = data["ticker"]["last"]
        volume = data["ticker"]["vol"]
        timestamp = datetime.utcfromtimestamp(float(data["date"]))

        return super(OKCoinFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
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
