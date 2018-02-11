"""FormattedResponse Class for Standardized methods of the Bitstamp Interface class."""
# Import Built-ins
from datetime import datetime
import pytz

# Import Home-brewed
from bitex.formatters.base import APIResponse


class BitstampFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)

        bid = data["bid"]
        ask = data["ask"]
        high = data["high"]
        low = data["low"]
        last = data["last"]
        volume = data["volume"]
        timestamp = datetime.utcfromtimestamp(float(data["timestamp"]))
        return super(BitstampFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                             timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def trades(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def bid(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        oid, ts, side = data['id'], data['datetime'], 'ask' if data['type'] else 'bid'
        price, size = data['price'], data['amount']
        return super(BitstampFormattedResponse, self).bid(oid, price, size, side, 'N/A', ts)

    def ask(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        oid, ts, side = data['id'], data['datetime'], 'ask' if data['type'] else 'bid'
        price, size = data['price'], data['amount']
        return super(BitstampFormattedResponse, self).ask(oid, price, size, side, 'N/A', ts)

    def order_status(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        state = data['status']
        oid = self.method_args[0]
        ts = self.received_at
        return super(BitstampFormattedResponse, self).order_status(
            oid, 'N/A', 'N/A', 'N/A', 'N/A', state, ts)

    def cancel_order(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=float)
        extracted_data = (data['id'], True if ('error' in data and data['error']) else False,
                          data['datetime'], data['error'] if 'error' in data else None)
        return super(BitstampFormattedResponse, self).cancel_order(*extracted_data)

    def open_orders(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        unpacked_orders = []
        for order in data:
            if order['type']:
                side = 'ask'
            else:
                side = 'bid'
            if 'pair' in self.method_kwargs:
                unpacked_order = (data['id'], self.method_kwargs['pair'], data['price'],
                                  data['amount'], side, data['datetime'])
            else:
                unpacked_order = (data['id'], data['currency_pair'], data['price'], data['amount'],
                                  side, data['datetime'])
            unpacked_orders.append(unpacked_order)

        ts = self.received_at
        return super(BitstampFormattedResponse, self).open_orders(unpacked_orders, ts)

    def wallet(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        return super(BitstampFormattedResponse, self).wallet(data, self.received_at)
