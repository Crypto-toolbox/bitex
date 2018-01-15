"""Interface Test Cases.

Interface test cases are classes that test basic functionality of extended core methods.

These methods include:
    - request()
    - is_supported()
    - _get_supported_pairs()


Tests for formatted responses and the standardized methods can be found in standard_method_tests.py
"""
# Import Built-Ins
import logging
import unittest
from unittest.mock import patch
import time


# Import Third-Party

# Import Homebrew
from .helpers import MockResponse, StandardizedMethodTests

from bitex.interface.rest import RESTInterface
from bitex.interface import Binance, Bitfinex, Bitstamp, Bittrex, CCEX
from bitex.interface import CoinCheck, Cryptopia, HitBTC, Kraken, OKCoin
from bitex.interface import Poloniex, QuadrigaCX, TheRockTrading, Vaultoro
from bitex.exceptions import UnsupportedEndpointError

# Init Logging Facilities
log = logging.getLogger(__name__)

tests_folder_dir = '.'


class BitfinexInterfacTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Bitfinex(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(['this', 'is', 'a', 'list'], 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Bitfinex()
        mocked_request_func.assert_called_with('GET', 'https://api.bitfinex.com/v1/symbols')
        self.assertEqual(b.supported_pairs, ['this', 'is', 'a', 'list'])

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)


class SMTBinance(StandardizedMethodTests):
    def __init__(self, *args, **kwargs):
        super(SMTBinance, self).__init__(Binance, *args, **kwargs)

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Bitfinex(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(['this', 'is', 'a', 'list'], 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Bitfinex()
        mocked_request_func.assert_called_with('GET', 'https://api.binance.com/api/v1/exchangeInfo')
        self.assertEqual(b.supported_pairs, ['this', 'is', 'a', 'list'])

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_wallet_formatter(expected_result, mock_json)


class BitstampInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class BittrexInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class CCEXInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class CoinCheckInterfaceTests(unittest.TestCase):
    def tearDown(self):
        time.sleep(1)


class CryptopiaInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class HitBTCInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class KrakenInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class OKCoinInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class PoloniexInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class QuadrigaCXInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class TheRockTradingInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


class VaultoroInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
