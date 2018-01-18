# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class PoloniexFormattedResponse(APIResponse):

    def ticker(self, *args):
        # The Poloniex public ticker returns a json containing the ticker of all the pairs traded
        # on the exchange. This is why we had to store the arguments passed to the method (ticker,
        # ask, etc..) of the Poloniex class, in order to extract the pair the user wants, and
        # format it in the correct way.
        all_pairs_tickers = self.json(parse_int=str, parse_float=str)
        _, pair_requested = self.method_args[:2]

        data = all_pairs_tickers[pair_requested]
        bid = data["highestBid"]
        ask = data["lowestAsk"]
        high = data["high24hr"]
        low = data["low24hr"]
        last = data["last"]
        volume = data["quoteVolume"]
        timestamp = datetime.utcnow()
        return super(PoloniexFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
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
