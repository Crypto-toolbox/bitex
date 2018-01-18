from bitex.formatters.base import APIResponse

from decimal import Decimal
from datetime import datetime


class BinanceFormattedResponse(APIResponse):

    def ticker(self, *args):
        data = self.json(parse_int=str, parse_float=str)
        bid = Decimal(data["bidPrice"]),
        ask = Decimal(data["askPrice"]),
        high = Decimal(data["highPrice"]),
        low = Decimal(data["lowPrice"]),
        last = Decimal(data["lastPrice"]),
        volume = Decimal(data["volume"]),
        timestamp = datetime.utcnow()
        return super(BinanceFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                            timestamp)

