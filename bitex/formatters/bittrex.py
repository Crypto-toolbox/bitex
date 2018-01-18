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

        dt = data["TimeStamp"]
        curr_timestamp = pytz.utc.localize(datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f'))

        bid = data["Bid"]
        ask = data["Ask"]
        high = data["High"]
        low = data["Low"]
        last = data["Last"]
        volume = data["Volume"]
        timestamp = curr_timestamp
        
        return super(BittrexFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                            timestamp)
