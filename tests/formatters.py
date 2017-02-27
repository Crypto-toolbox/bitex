# Import Built-Ins
import logging
from unittest import TestCase
# Import Third-Party

# Import Homebrew
from bitex.formatters.kraken import KrknFormatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class FormatterTest(TestCase):
    def test_format_pair_works_correctly(self):
        fmt = KrknFormatter()
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'xxbtxltc']
        expected_output = ['XXBTZUSD', 'XLTCXXBT', 'XXMRXXBT', 'XXBTXLTC']
        fmt_output = [fmt.format_pair(pair) for pair in test_pairs]
        self.assertEqual(fmt_output, expected_output)
