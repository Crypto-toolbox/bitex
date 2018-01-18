from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime

fromtimestamp = datetime.utcfromtimestamp


class OKCoinFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)

        return TickerFormattedResponseTuple(bid=Decimal(data["ticker"]["buy"]),
                                            ask=Decimal(data["ticker"]["sell"]),
                                            high=Decimal(data["ticker"]["high"]),
                                            low=Decimal(data["ticker"]["low"]),
                                            last=Decimal(data["ticker"]["last"]),
                                            volume=Decimal(data["ticker"]["vol"]),
                                            timestamp=fromtimestamp(Decimal(data["date"])),
                                            )
