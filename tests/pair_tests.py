# Import Built-Ins
import logging
import unittest
# Import Third-Party

# Import Homebrew
from bitex.pairs import PairFormatter()
# Init Logging Facilities
log = logging.getLogger(__name__)


class PairTests(unittest.TestCase):
    def test_that_pair_class_returns_correct_format(self):
        pair = PairFormatter('BTCUSD')

        # Assert All exchanges are supported and formatted correctly
        self.assertEqual(pair.format('Kraken'), 'XXBTZUSD')
        self.assertEqual(pair.format('Poloniex'), 'BTC_USD')

        # Assert that calling the formatter returns the standard presentation
        self.assertEqual(pair(), 'BTCUSD')

