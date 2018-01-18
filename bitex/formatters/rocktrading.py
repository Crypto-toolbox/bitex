# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class RockTradingFormattedResponse(APIResponse):

    def ticker(self, *args):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        bid = data["bidPrice"]
        ask = data["askPrice"]
        high = data["highPrice"]
        low = data["lowPrice"]
        last = data["lastPrice"]
        volume = data["volume"]
        timestamp = datetime.utcnow()
        return super(RockTradingFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                                timestamp)

    def order_book(self, bids, asks, ts):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def trades(self, trades, ts):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def bid(self, price, size, side, oid, otype, ts):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def ask(self, price, size, side, oid, otype, ts):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def order_status(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def cancel_order(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def open_orders(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def wallet(self, *args):
        """Return namedtuple with given data."""
        raise NotImplementedError
