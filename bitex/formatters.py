#   Import Built-ins
from itertools import chain


ttable = {'Kraken': {'XBTEUR': 'XXBTZEUR', 'XBTUSD': 'XXBTZUSD',
                     'XRPXBT': 'XXRPXXBT', 'REPXBT': 'XREPXXBT'},
          'Bitfinex': {},
          'Bitstamp': {},
          'Bittrex': {},
          'Coincheck': {},
          'Cryptopia': {},
          'Gemini': {},
          'itBit': {},
          'OKCoin': {},
          'RockTradingLtd': {}}

#  Add revert translations to ttable
for ex in ttable:
    for key, val in ttable[ex].items():
        ttable[ex][val] = key


class Formatter:
    def __init__(self, translation_table):
        """

        :param translation_table: Dict of key value pairs that enable the
        formatter to convert pair names.
        """
        self._ttable = translation_table

    def order_book(self, data):
        """
        Returs tuple of lists, bids and asks respectively,  as follows:
        ([(exchange, pair, ts, price, vol), ...],
        [(exchange, pair, ts, price, vol), ...])
        :param data:
        :return:
        """
        bids, asks = [], []
        return bids, asks

    def ticker(self, data):
        pass

    def trades(self, data):
        pass


class KrakenFormatter(Formatter):
    def __init__(self):
        super(KrakenFormatter, self).__init__(ttable['Kraken'])

    def format_order_book(self, data):
        pair_data = data['result']
        error = data['error']
        pair = list(pair_data.keys())
        if len(pair) > 1:
            raise NotImplementedError("KrakenFormatter.format_order_book() "
                                      "does not support order book dicts with "
                                      "multiple pairs, yet!")

        bids, asks = pair_data[pair]['bids'], pair_data[pair]['asks']
        for i, bid in enumerate(bids):
            price, vol, ts = bid
            bids[i] = ['Kraken', self._ttable[pair], price, vol, ts]

        for i, ask in enumerate(asks):
            price, vol, ts = ask
            asks[i] = ['Kraken', self._ttable[pair], price, vol, ts]

        return bids, asks

    def format_trades(self, data):
        pair_data = data['result']
        pair = list(pair_data.keys())
        if len(pair) > 1:
            raise NotImplementedError("KrakenFormatter.format_trades() "
                                      "does not support trades dicts with "
                                      "multiple pairs, yet!")
        trades = pair_data[pair]
        for i in range(len(trades)):
            price, vol, ts, side, order_type, etc
            trades[i] = ['Kraken', self._ttable[pair], price, vol, ts, side,
                         order_type, etc]
        return trades

    def format_ticker(self, data):
        return ticker

