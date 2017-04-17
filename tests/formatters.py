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


class FormatterTestCase(TestCase):
    def setUp(self):
        self.formatter = None

    def test_format_pair_works_correctly(self, test_pairs, expected):
        fmt_output = [self.formatter.format_pair(pair) for pair in test_pairs]
        self.assertEqual(fmt_output, expected)

    def test_ticker_formatter(self, input_data, expected_output):
        output = self.formatter.ticker(input_data)
        self.assertEqual(output, expected_output)

    def test_order_book_formatter(self, input_data, expected_output):
        output = self.formatter.ticker(input_data)
        self.assertEqual(output, expected_output)

    def test_trades_formatter(self, input_data, expected_output):
        output = self.formatter.trades(input_data)
        self.assertEqual(output, expected_output)

    def test_order_formatter(self, input_data, expected_output):
        output = self.formatter.order(input_data)
        self.assertEqual(output, expected_output)

    def test_order_status_formatter(self, input_data, expected_output):
        output = self.formatter.order_status(input_data)
        self.assertEqual(output, expected_output)

    def test_cancel_formatter(self, input_data, expected_output):
        output = self.formatter.cancel(input_data)
        self.assertEqual(output, expected_output)

    def test_balance_formatter(self, input_data, expected_output):
        output = self.formatter.balance(input_data)
        self.assertEqual(output, expected_output)

    def test_withdraw_formatter(self, input_data, expected_output):
        output = self.formatter.withdraw(input_data)
        self.assertEqual(output, expected_output)

    def test_deposit_formatter(self, input_data, expected_output):
        output = self.formatter.deposit(input_data)
        self.assertEqual(output, expected_output)


class KrakenFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = KrknFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'xxbtxltc', 'DaShBTC',
                      'dasheur']
        expected_output = ['XXBTZUSD', 'XLTCXXBT', 'XXMRXXBT', 'XXBTXLTC',
                           'DASHXXBT', 'DASHZEUR']
        super(KrakenFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class BitstampFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtstFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR']
        expected_output = ['btcusd', 'ltcbtc', 'xmrbtc', 'btceur']
        super(BitstampFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class BitfinexFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtfxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR']
        expected_output = ['BTCUSD', 'LTCBTC', 'XMRBTC', 'BTCEUR']
        super(BitfinexFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class BittrexFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR']
        expected_output = ['BTC-USD', 'BTC-LTC', 'XMR-BTC', 'BTC-EUR']
        super(BittrexFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)
