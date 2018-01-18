from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime

fromtimestamp = datetime.utcfromtimestamp


class CCEXFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)
        data = data["ticker"]

        # CCEX does not provide volume metrics.
        # {'high': Decimal('0.00007307'), 'low': Decimal('0.00006667'),
        #  'avg': Decimal('0.00006987'), 'lastbuy': Decimal('0.00007097'),
        #  'lastsell': Decimal('0.00007146'), 'buy': Decimal('0.00007098'),
        #  'sell': Decimal('0.00007145'), 'lastprice': Decimal('0.00007146'),
        #  'buysupport': Decimal('22.39634869'), 'updated': Decimal('1515768078')}

        return TickerFormattedResponseTuple(bid=Decimal(data["lastbuy"]),
                                            ask=Decimal(data["lastsell"]),
                                            high=Decimal(data["high"]),
                                            low=Decimal(data["low"]),
                                            last=Decimal(data["lastprice"]),
                                            volume=None,
                                            timestamp=fromtimestamp(Decimal(data["updated"]))
                                            )
