# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class BitstampFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)

        bid = data["bid"]
        ask = data["ask"]
        high = data["high"]
        low = data["low"]
        last = data["last"]
        volume = data["volume"]
        timestamp = datetime.utcfromtimestamp(data["timestamp"])
        return super(BitstampFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                             timestamp)