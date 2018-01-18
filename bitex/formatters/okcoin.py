# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class OKCoinFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)
        bid = data["ticker"]["buy"]
        ask = data["ticker"]["sell"]
        high = data["ticker"]["high"]
        low = data["ticker"]["low"]
        last = data["ticker"]["last"]
        volume = data["ticker"]["vol"]
        timestamp = datetime.utcfromtimestamp(data["date"])

        return super(OKCoinFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                             timestamp)
