from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime

fromtimestamp = datetime.fromtimestamp


class BitfinexFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        # {'bid': '14827.0', 'ask': '14828.0', 'high': '14961.0', 'low': '11730.0',
        #  'last_price': '14829.0', 'volume': '87898.99047435', 'timestamp': '1514042460.7861257',
        #  'mid': '14827.5'}
        data = self.json(parse_int=Decimal, parse_float=Decimal)

        return TickerFormattedResponseTuple(bid=Decimal(data["bid"]),
                                            ask=Decimal(data["ask"]),
                                            high=Decimal(data["high"]),
                                            low=Decimal(data["low"]),
                                            last=Decimal(data["last_price"]),
                                            volume=Decimal(data["volume"]),
                                            timestamp=fromtimestamp(float(data["timestamp"]))
                                            )
