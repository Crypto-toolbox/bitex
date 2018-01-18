from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal


class KrakenFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=Decimal, parse_float=Decimal)

        # return TickerFormattedResponseTuple(bid=Decimal(data["bid"]),
        #                                     ask=Decimal(data["ask"]),
        #                                     high=Decimal(data["high"]),
        #                                     low=Decimal(data["low"]),
        #                                     last=Decimal(data["last"]),
        #                                     volume=Decimal(data["volume"]),
        #                                     timestamp=data["timestamp"] / Decimal(1000),
        #                                     )
        raise NotImplementedError
