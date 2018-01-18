# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse



class CCEXFormattedResponse(APIResponse):

    def ticker(self):
        data = self.json(parse_int=str, parse_float=str)
        data = data["ticker"]

        # CCEX does not provide volume metrics.
        # {'high': '0.00007307'), 'low': '0.00006667'),
        #  'avg': '0.00006987'), 'lastbuy': '0.00007097'),
        #  'lastsell': '0.00007146'), 'buy': '0.00007098'),
        #  'sell': '0.00007145'), 'lastprice': '0.00007146'),
        #  'buysupport': '22.39634869'), 'updated': '1515768078')}

        bid = data["lastbuy"]
        ask = data["lastsell"]
        high = data["high"]
        low = data["low"]
        last = data["lastprice"]
        volume = None,
        timestamp = datetime.utcfromtimestamp(data["updated"])
        return super(CCEXFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                         timestamp)
