"""FormattedResponse Class for Standardized methods of the GDAX Interface class."""
# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class GDAXFormattedResponse(APIResponse):
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
        return super(GDAXFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                         timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def trades(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def bid(self):
        """Return namedtuple with given data.

        sample response:
            {
                "id": "d0c5340b-6d6c-49d9-b567-48c4bfca13d2",
                "price": "0.10000000",
                "size": "0.01000000",
                "product_id": "BTC-USD",
                "side": "buy",
                "stp": "dc",
                "type": "limit",
                "time_in_force": "GTC",
                "post_only": false,
                "created_at": "2016-12-08T20:02:28.53864Z",
                "fill_fees": "0.0000000000000000",
                "filled_size": "0.00000000",
                "executed_value": "0.0000000000000000",
                "status": "pending",
                "settled": false
            }
        """
        data = self.json(parse_int=str, parse_float=str)
        oid, price, size = data['id'], data['price'], data['size']
        side, otype, ts = data['side'], data['type'], data['created_at']
        return super(GDAXFormattedResponse, self).ask(oid, price, size, side, otype, ts)

    def ask(self):
        """Return namedtuple with given data.

        sample response:
            {
                "id": "d0c5340b-6d6c-49d9-b567-48c4bfca13d2",
                "price": "0.10000000",
                "size": "0.01000000",
                "product_id": "BTC-USD",
                "side": "buy",
                "stp": "dc",
                "type": "limit",
                "time_in_force": "GTC",
                "post_only": false,
                "created_at": "2016-12-08T20:02:28.53864Z",
                "fill_fees": "0.0000000000000000",
                "filled_size": "0.00000000",
                "executed_value": "0.0000000000000000",
                "status": "pending",
                "settled": false
            }
        """
        data = self.json(parse_int=str, parse_float=str)
        oid, price, size = data['id'], data['price'], data['size']
        side, otype, ts = data['side'], data['type'], data['created_at']
        return super(GDAXFormattedResponse, self).ask(oid, price, size, side, otype, ts)

    def order_status(self):
        """Return namedtuple with given data.

        sample:
        {
            "id": "68e6a28f-ae28-4788-8d4f-5ab4e5e5ae08",
            "size": "1.00000000",
            "product_id": "BTC-USD",
            "side": "buy",
            "stp": "dc",
            "funds": "9.9750623400000000",
            "specified_funds": "10.0000000000000000",
            "type": "market",
            "post_only": false,
            "created_at": "2016-12-08T20:09:05.508883Z",
            "done_at": "2016-12-08T20:09:05.527Z",
            "done_reason": "filled",
            "fill_fees": "0.0249376391550000",
            "filled_size": "0.01291771",
            "executed_value": "9.9750556620000000",
            "status": "done",
            "settled": true
        }
        """
        data = self.json(parse_int=str, parse_float=str)
        oid, price, size = data['id'], data['price'], data['size']
        side, otype, state = data['side'], data['type'], data['status']
        ts = data['created_at']
        return super(GDAXFormattedResponse, self).order_status(
            oid, price, size, side, otype, state, ts)

    def cancel_order(self):
        """Return namedtuple with given data.

        "If the order could not be canceled (already filled or previously canceled, etc),
        then an error response will indicate the reason in the message field."
        """
        data = self.json()
        if 'message' in data:
            return super(GDAXFormattedResponse, self).cancel_order(
                self.method_args[0], False, self.received_at, data['message'])
        else:
            return super(GDAXFormattedResponse, self).cancel_order(
                self.method_args[0], True, self.received_at, None)

    def open_orders(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        return super(GDAXFormattedResponse, self).open_orders(data, self.received_at)

    def wallet(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        balances = {d['currency']: d['available'] for d in data}
        return super(GDAXFormattedResponse, self).wallet(balances, self.received_at)
