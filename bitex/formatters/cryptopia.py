from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime


class CryptopiaFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)
        data = data["Data"]

        return TickerFormattedResponseTuple(bid=Decimal(data["BidPrice"]),
                                            ask=Decimal(data["AskPrice"]),
                                            high=Decimal(data["High"]),
                                            low=Decimal(data["Low"]),
                                            last=Decimal(data["LastPrice"]),
                                            volume=Decimal(data["Volume"]),
                                            timestamp=datetime.utcnow()
                                            )
