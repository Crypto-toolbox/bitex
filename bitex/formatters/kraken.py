from bitex.formatters.base import APIResponse


class KrakenFormattedResponse(APIResponse):

    @property
    def ticker(self):
        """Return namedtuple with given data."""
        # data = self.json(parse_int=str, parse_float=str)

        # return TickerFormattedResponseTuple(bid=Decimal(data["bid"]),
        #                                     ask=Decimal(data["ask"]),
        #                                     high=Decimal(data["high"]),
        #                                     low=Decimal(data["low"]),
        #                                     last=Decimal(data["last"]),
        #                                     volume=Decimal(data["volume"]),
        #                                     timestamp=data["timestamp"] / Decimal(1000),
        #                                     )
        raise NotImplementedError

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
