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


# Import Third-Party

# Import Homebrew
from helpers import MockResponse, StandardizedMethodTests
from payloads import rock_trading_tickers_parsed, kraken_asset_pairs_parsed, poloniex_tickers_parsed
from payloads import hitbtc_symbols_parsed, cryptopia_trade_pairs_parsed, ccex_pairs_parsed
from payloads import bittrex_getmarkets_parsed, bitstamp_trading_pairs_parsed
from payloads import binance_exchange_info_parsed, bitfinex_symbols_parsed
from bitex.interface.rest import RESTInterface
from bitex.interface import Binance, Bitfinex, Bitstamp, Bittrex, CCEX
from bitex.interface import CoinCheck, Cryptopia, HitBTC, Kraken, OKCoin
from bitex.interface import Poloniex, QuadrigaCX, TheRockTrading, Vaultoro

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

    @patch('requests.request', return_value=MockResponse(bitfinex_symbols_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Bitfinex()
        mocked_request_func.assert_called_with('GET', 'https://api.bitfinex.com/v1/symbols')
        expected_list = sorted(bitfinex_symbols_parsed)
        self.assertEqual(sorted(b.supported_pairs), expected_list)

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


class BinanceInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Binance(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(binance_exchange_info_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Binance()
        mocked_request_func.assert_called_with('GET', 'https://api.binance.com/api/v1/exchangeInfo')
        expected_list = sorted([d['symbol'] for d in binance_exchange_info_parsed['symbols']])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class BitstampInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Bitstamp(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(bitstamp_trading_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Bitstamp()
        mocked_request_func.assert_called_with('GET', 'https://www.bitstamp.net/api/v2/trading-pairs-info/')
        expected_list = sorted([d['url_symbol'] for d in bitstamp_trading_pairs_parsed])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitstampInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class BittrexInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Bittrex(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(bittrex_getmarkets_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Bittrex()
        mocked_request_func.assert_called_with('GET', 'https://bittrex.com/api/v1.1/public/getmarkets')
        expected_list = sorted([d['MarketName'] for d in bittrex_getmarkets_parsed['result']])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BittrexInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class CCEXInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = CCEX(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(ccex_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = CCEX()
        mocked_request_func.assert_called_with('GET', 'https://c-cex.com/t/pairs.json')
        expected_list = sorted(ccex_pairs_parsed['pairs']])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CCEXInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class CoinCheckInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = CoinCheck(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        self.assertEqual(['btc-jpy'], CoinCheck()._get_supported_pairs())

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CoinCheckInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class CryptopiaInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Cryptopia(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(cryptopia_trade_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Cryptopia()
        mocked_request_func.assert_called_with('GET', 'https://www.cryptopia.co.nz/api/GetTradePairs')
        expected_list = [d['Label'] for d in cryptopia_trade_pairs_parsed['Data']]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(CryptopiaInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class HitBTCInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = HitBTC(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(hitbtc_symbols_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = HitBTC()
        mocked_request_func.assert_called_with('GET', 'https://api.hitbtc.com/api/2/public/symbol')
        expected_list = [entry['id'] for entry in hitbtc_symbols_parsed]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(HitBTCInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class KrakenInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Kraken(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(kraken_asset_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Kraken()
        mocked_request_func.assert_called_with('GET', 'https://api.kraken.com/0/public/AssetPairs')
        expected_list = [pair for pair in kraken_asset_pairs_parsed['result']]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(KrakenInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class OKCoinInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = OKCoin(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        pairs = OKCoin()._get_supported_pairs()
        self.assertEqual(pairs, ['btc_usd', 'ltc_usd', 'eth_usd', 'etc_usd', 'bch_usd', 'btc_cny',
                                 'ltc_cny', 'eth_cny', 'etc_cny', 'bch_cny'])

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(OKCoinInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class PoloniexInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Poloniex(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(poloniex_tickers_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Poloniex()
        mocked_request_func.assert_called_with('GET', 'https://poloniex.com/public?command=returnTicker')
        expected_list = [pair for pair in poloniex_tickers_parsed]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(PoloniexInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class QuadrigaCXInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = QuadrigaCX(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        b = QuadrigaCX()
        expected_list = 'btc_cad,btc_usd,eth_cad,eth_btc,ltc_cad,ltc_btc,bch_cad,bch_btc,btg_cad,btg_btc'.split(',')
        self.assertEqual(b._get_supported_pairs(), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuadrigaCXInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class TheRockTradingInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = TheRockTrading(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(rock_trading_tickers_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = TheRockTrading()
        mocked_request_func.assert_called_with('GET', 'https://api.therocktrading.com/v1/funds/tickers')
        expected_list = [t['fund_id'] for t in rock_trading_tickers_parsed['tickers']]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class VaultoroInterfaceTests(StandardizedMethodTests):

    @patch(RESTInterface, 'request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Vaultoro(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        b = Vaultoro()
        self.assertEqual(b._get_supported_pairs(), ['BTC-GLD'])

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(VaultoroInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


if __name__ == '__main__':
    unittest.main(verbosity=2)
