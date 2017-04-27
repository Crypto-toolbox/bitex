# Import Built-Ins
import logging
from unittest import TestCase
# Import Third-Party

# Import Homebrew
from bitex.formatters.bitfinex import BtfxFormatter
from bitex.formatters.bitstamp import BtstFormatter
from bitex.formatters.bittrex import BtrxFormatter
from bitex.formatters.bter import BterFormatter
from bitex.formatters.ccex import CcexFormatter
from bitex.formatters.coincheck import CnckFormatter
from bitex.formatters.cryptopia import CrptFormatter
from bitex.formatters.gdax import GdaxFormatter
from bitex.formatters.gemini import GmniFormatter
from bitex.formatters.hitbtc import HitBtcFormatter
from bitex.formatters.itbit import itbtFormatter
from bitex.formatters.kraken import KrknFormatter
from bitex.formatters.okcoin import OkcnFormatter
from bitex.formatters.poloniex import PlnxFormatter
from bitex.formatters.quadriga import QuadrigaCXFormatter
from bitex.formatters.quoine import QoinFormatter
from bitex.formatters.rocktrading import RockFormatter
from bitex.formatters.vaultoro import VaultoroFormatter
from bitex.formatters.yunbi import YnbiFormatter



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
        expected_output = ['BTC-USD', 'LTC-BTC', 'XMR-BTC', 'BTC-EUR']
        super(BittrexFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class BterFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BterFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc_usd', 'ltc_btc', 'xmr_btc', 'btc_eur', 'qtum_eth']
        super(BterFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class CCEXFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc-usd', 'ltc-btc', 'xmr-btc', 'btc-eur', 'qtum-eth']
        super(CCEXFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class CoinCheckFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc_usd', 'ltc_btc', 'xmr_btc', 'btc_eur', 'qtum-eth']
        super(CoinCheckFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class CryptopiaFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'dashuno']
        expected_output = [None, 101, 2999, None, None]
        super(CryptopiaFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class GDAXFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['BTC-USD', 'LTC-BTC', 'XMR-BTC', 'BTC-EUR', 'QTUM-ETH']
        super(GDAXFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class GeminiFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btcusd', 'ltcbtc', 'xmrbtc', 'btceur', 'qtumeth']
        super(GeminiFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class HitBtcFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['BTCUSD', 'LTCBTC', 'XMRBTC', 'BTCEUR', 'QTUMETH']
        super(HitBtcFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class ItBitFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['BTCUSD', 'LTCBTC', 'XMRBTC', 'BTCEUR', 'QTUMETH']
        super(ItBitFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class OKCoinFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc_usd', 'ltc_btc', 'xmr_btc', 'btc_eur', 'qtum_eth']
        super(OKCoinFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class PoloniexFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['BTC_USD', 'LTC_BTC', 'XMR_BTC', 'BTC_EUR', 'QTUM_ETH']
        super(PoloniexFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class QuadrigaCXFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc_usd', 'ltc_btc', 'xmr_btc', 'btc_eur', 'qtum_eth']
        super(QuadrigaCXFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class QuoineFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['BTCUSD', 'LTCBTC', 'XMRBTC', 'BTCEUR', 'QTUMETH']
        super(QuoineFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class RockTradingFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['BTCUSD', 'LTCBTC', 'XMRBTC', 'BTCEUR', 'QTUMETH']
        super(RockTradingFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class VaultoroFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc_usd', 'ltc_btc', 'xmr_btc', 'btc_eur', 'qtum_eth']
        super(VaultoroFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)


class YunbiFormatterTest(FormatterTestCase):
    def setUp(self):
        self.formatter = BtrxFormatter()

    def test_format_pair_works_correctly(self):
        test_pairs = ['btcusd', 'ltcbtc', 'xmr_btc', 'BTCEUR', 'qtumeth']
        expected_output = ['btc_usd', 'ltc_btc', 'xmr_btc', 'btc_eur', 'qtum_eth']
        super(YunbiFormatterTest, self).test_format_pair_works_correctly(
            test_pairs, expected_output)