from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime

fromtimestamp = datetime.utcfromtimestamp


class HitBTCFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)

        curr_timestamp = fromtimestamp(data["timestamp"] / Decimal(1000))

        return TickerFormattedResponseTuple(bid=Decimal(data["bid"]),
                                            ask=Decimal(data["ask"]),
                                            high=Decimal(data["high"]),
                                            low=Decimal(data["low"]),
                                            last=Decimal(data["last"]),
                                            volume=Decimal(data["volume"]),
                                            timestamp=curr_timestamp,
                                            )
