# Import Built-Ins
import logging
from unittest import TestCase
# Import Third-Party

# Import Homebrew
from bitex.formatters.kraken import KrknFormatter
from bitex.formatters.bitfinex import BtfxFormatter
from bitex.formatters.bitstamp import BtstFormatter
from bitex.formatters.bittrex import BtrxFormatter


# Init Logging Facilities
log = logging.getLogger(__name__)


class FormatterTest(TestCase):
    def test_krknFormatter_format_pair_works_correctly(self):
        fmt = KrknFormatter()
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'xxbtxltc', 'DaShBTC',
                      'dasheur']
        expected_output = ['XXBTZUSD', 'XLTCXXBT', 'XXMRXXBT', 'XXBTXLTC',
                           'DASHXXBT', 'DASHZEUR']
        fmt_output = [fmt.format_pair(pair) for pair in test_pairs]
        self.assertEqual(fmt_output, expected_output)

    def test_BtstFormatter_format_pair_works_correctly(self):
        fmt = BtstFormatter()
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR']
        expected_output = ['btcusd', 'ltcbtc', 'xmrbtc', 'btceur']
        fmt_output = [fmt.format_pair(pair) for pair in test_pairs]
        self.assertEqual(fmt_output, expected_output)

    def test_BtfxFormatter_format_pair_works_correctly(self):
        fmt = BtfxFormatter()
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR']
        expected_output = ['BTCUSD', 'LTCBTC', 'XMRBTC', 'BTCEUR']
        fmt_output = [fmt.format_pair(pair) for pair in test_pairs]
        self.assertEqual(fmt_output, expected_output)

    def test_BtrxFormatter_format_pair_works_correctly(self):
        fmt = BtrxFormatter()
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR']
        expected_output = ['BTC-USD', 'BTC-LTC', 'XMR-BTC', 'BTC-EUR']
        fmt_output = [fmt.format_pair(pair) for pair in test_pairs]
        self.assertEqual(fmt_output, expected_output)