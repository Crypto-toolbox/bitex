from bitex.formatters.base import APIResponse


class KrakenFormattedResponse(APIResponse):

    @property
    def ticker(self):
        data = self.json(parse_int=str, parse_float=str)

        # return TickerFormattedResponseTuple(bid=Decimal(data["bid"]),
        #                                     ask=Decimal(data["ask"]),
        #                                     high=Decimal(data["high"]),
        #                                     low=Decimal(data["low"]),
        #                                     last=Decimal(data["last"]),
        #                                     volume=Decimal(data["volume"]),
        #                                     timestamp=data["timestamp"] / Decimal(1000),
        #                                     )
        raise NotImplementedError
