# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class CryptopiaFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)
        data = data["Data"]
        
        bid = data["BidPrice"]
        ask = data["AskPrice"]
        high = data["High"]
        low = data["Low"]
        last = data["LastPrice"]
        volume = data["Volume"]
        timestamp = datetime.utcnow()

        return super(CryptopiaFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                              timestamp)
