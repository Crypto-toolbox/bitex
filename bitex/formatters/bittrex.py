# Import Built-ins
from datetime import datetime

# Import third-party
import pytz

# Import Home-brewed
from bitex.formatters.base import APIResponse


class BittrexFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)
        data = data["result"][0]

        dt_str = data["TimeStamp"]
        curr_timestamp = pytz.utc.localize(datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f'))

        bid = data["Bid"]
        ask = data["Ask"]
        high = data["High"]
        low = data["Low"]
        last = data["Last"]
        volume = data["Volume"]
        timestamp = curr_timestamp

        return super(BittrexFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
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
