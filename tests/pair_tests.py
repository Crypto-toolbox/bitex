# Import Built-Ins
import logging
import unittest
# Import Third-Party

# Import Homebrew
from bitex.pairs import PairFormatter
# Init Logging Facilities
log = logging.getLogger(__name__)


class PairTests(unittest.TestCase):
    def test_that_pair_class_returns_correct_format(self):
        pair = PairFormatter('BTC', 'USD')

        # Assert All exchanges are supported and format correctly;
        # This excludes edge cases, which are tested separately
        self.assertEqual(pair.format('Kraken'), 'XXBTZUSD')
        self.assertEqual(pair.format('Bitstamp'), 'btcusd')
        self.assertEqual(pair.format('Bitfinex'), 'BTCUSD')
        self.assertEqual(pair.format('Bittrex'), 'BTC-USD')
        self.assertEqual(pair.format('CoinCheck'), 'BTCUSD')
        self.assertEqual(pair.format('GDAX'), 'BTC-USD')
        self.assertEqual(pair.format('ITBit'), 'XBTUSD')
        self.assertEqual(pair.format('OKCoin'), 'btc_usd')
        self.assertEqual(pair.format('BTC-E'), 'btc_usd')
        self.assertEqual(pair.format('C-CEX'), 'BTC/USD')
        self.assertEqual(pair.format('Cryptopia'), 'BTC_USD')
        self.assertEqual(pair.format('Gemini'), 'btcusd')
        self.assertEqual(pair.format('Yunbi'), 'btcusd')
        self.assertEqual(pair.format('The Rock Trading Ltd.'), 'BTCUSD')
        self.assertEqual(pair.format('Poloniex'), 'BTC_USD')
        self.assertEqual(pair.format('Quoine'), 'BTCUSD')
        self.assertEqual(pair.format('QuadrigaCX'), 'btc_usd')
        self.assertEqual(pair.format('HitBTC'), 'BTCUSD')
        self.assertEqual(pair.format('Vaultoro'), 'BTC-USD')
        self.assertEqual(pair.format('Bter'), 'btc_usd')

        # Assert that calling the formatter returns the standard presentation
        self.assertEqual(pair(), 'BTCUSD')

    def test_poloniex_formatter_edge_case(self):
        # Assert that BTC in quote is swapped to base
        pair = PairFormatter('LTC', 'BTC')
        self.assertEqual(pair.format('Poloniex'), 'BTC_LTC')

        # Assert that USDT is swapped from quote to base
        pair = PairFormatter('LTC', 'USDT')
        self.assertEqual(pair.format('Poloniex'), 'USDT_LTC')

        # Assert that XMR is only swapped to base if current base is not BTC or
        # USDT
        pair = PairFormatter('BTC', 'XMR')
        self.assertEqual(pair.format('Poloniex'), 'BTC_XMR')
        pair = PairFormatter('USDT', 'XMR')
        self.assertEqual(pair.format('Poloniex'), 'USDT_XMR')
        pair = PairFormatter('ETH', 'XMR')
        self.assertEqual(pair.format('Poloniex'), 'XMR_ETH')

    def test_bitfinex_formatter_edge_case(self):
        # The DASH symbol is shortened in the Bitfinex API standard, hence
        # our formatter should take this into consideration
        pair = PairFormatter('DASH', 'USD')
        self.assertEqual(pair.format('Bitfinex'), 'DSHUSD')

        pair = PairFormatter('USD', 'DASH')
        self.assertEqual(pair.format('Bitfinex'), 'USDDSH')

    def test_kraken_formatter_edge_case(self):
        pair = PairFormatter('BCH', 'EUR')
        self.assertEqual(pair.format_for('Kraken'), 'BCHEUR')

if __name__ == '__main__':
    unittest.main()
