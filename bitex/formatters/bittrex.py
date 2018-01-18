from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime
import pytz

utc = pytz.utc


class BittrexFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)
        data = data["result"][0]

        dt = data["TimeStamp"]
        curr_timestamp = utc.localize(datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f'))

        return TickerFormattedResponseTuple(bid=Decimal(data["Bid"]),
                                            ask=Decimal(data["Ask"]),
                                            high=Decimal(data["High"]),
                                            low=Decimal(data["Low"]),
                                            last=Decimal(data["Last"]),
                                            volume=Decimal(data["Volume"]),
                                            timestamp=curr_timestamp,
                                            )
