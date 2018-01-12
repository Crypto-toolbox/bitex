from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime


class BinanceFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)

        return TickerFormattedResponseTuple(bid=Decimal(data["bidPrice"]),
                                            ask=Decimal(data["askPrice"]),
                                            high=Decimal(data["highPrice"]),
                                            low=Decimal(data["lowPrice"]),
                                            last=Decimal(data["lastPrice"]),
                                            volume=Decimal(data["volume"]),
                                            timestamp=datetime.utcnow()
                                            )
