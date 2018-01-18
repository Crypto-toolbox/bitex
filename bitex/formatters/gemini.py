# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class GeminiFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)
        bid = data["bidPrice"]
        ask = data["askPrice"]
        high = data["highPrice"]
        low = data["lowPrice"]
        last = data["lastPrice"]
        volume = data["volume"]
        timestamp = datetime.utcnow()
        return super(GeminiFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                           timestamp)
