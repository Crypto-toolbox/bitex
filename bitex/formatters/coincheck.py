from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime

fromtimestamp = datetime.utcfromtimestamp


class CoinCheckFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)

        return TickerFormattedResponseTuple(bid=Decimal(data["bid"]),
                                            ask=Decimal(data["ask"]),
                                            high=Decimal(data["high"]),
                                            low=Decimal(data["low"]),
                                            last=Decimal(data["last"]),
                                            volume=Decimal(data["volume"]),
                                            timestamp=fromtimestamp(Decimal(data["timestamp"]))
                                            )
