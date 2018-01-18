from bitex.formatters.base import AbstractFormattedResponse, TickerFormattedResponseTuple

from decimal import Decimal
from datetime import datetime


class PoloniexFormattedResponse(AbstractFormattedResponse):

    @property
    def ticker(self, *args, **kwargs):

        # The Poloniex public ticker returns a json containing the ticker of all the pairs traded
        # on the exchange. This is why we had to store the arguments passed to the method (ticker,
        # ask, etc..) of the Poloniex class, in order to extract the pair the user wants, and
        # format it in the correct way.
        all_pairs_tickers = self.json(parse_int=Decimal, parse_float=Decimal)
        _, pair_requested = self.method_args[:2]
        data = all_pairs_tickers[pair_requested]

        return TickerFormattedResponseTuple(bid=Decimal(data["highestBid"]),
                                            ask=Decimal(data["lowestAsk"]),
                                            high=Decimal(data["high24hr"]),
                                            low=Decimal(data["low24hr"]),
                                            last=Decimal(data["last"]),
                                            volume=Decimal(data["quoteVolume"]),
                                            timestamp=datetime.utcnow()
                                            )
