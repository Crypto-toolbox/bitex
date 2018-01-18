# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class HitBTCFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)

        curr_timestamp = datetime.utcfromtimestamp(data["timestamp"] / 1000)

        bid = data["bid"]
        ask = data["ask"]
        high = data["high"]
        low = data["low"]
        last = data["last"]
        volume = data["volume"]
        timestamp = curr_timestamp
        
        return super(HitBTCFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                           timestamp)
