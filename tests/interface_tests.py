"""Interface Test Cases.

Any methods that require a symbol pair are called with 'BTC-USD' - since the api calls are offline
this should not cause any error, even for exchanges that do not support that pair.
You must, however, properly patch _get_supported_pairs() of the exchange instance for
each test case:

    with patch('bitex.interface.vaultoro.Vaultoro._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Vaultoro(key='someKey', secret='some_secret')

It's important to pass credentials, as without them the Interface is designed to throw an exception
and not make the call.


"""
# Import Built-Ins
import logging
import unittest
from unittest.mock import patch


# Import Third-Party

# Import Homebrew
from tests.helpers import MockResponse, BaseInterfaceTests
from tests.payloads import *
from bitex.interface import Binance, Bitfinex, Bitstamp, Bittrex
from bitex.interface import CCEX, CoinCheck, Cryptopia
from bitex.interface import GDAX, Gemini, HitBTC, ItBit, Kraken, OKCoin
from bitex.interface import Poloniex, QuadrigaCX, Quoine, TheRockTrading, Vaultoro

# Init Logging Facilities
log = logging.getLogger(__name__)

tests_folder_dir = '.'


class BinanceInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.binance.Binance._get_supported_pairs',
               return_value=['BTC-USD']):
        exchange = Binance(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Binance(key='1231', secret='152561')
        api.request('POST', 'some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('GET', 'some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(binance_exchange_info_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Binance()
        mocked_request_func.assert_called_with('GET', 'https://api.binance.com/api/v1/exchangeInfo')
        expected_list = sorted([d['symbol'] for d in binance_exchange_info_parsed['symbols']])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = binance_ticker
        super(BinanceInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = binance_order_book
        super(BinanceInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = binance_trades
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
        kwargs = {'pair': 'BTC-USD'}
        expected_result = tuple()
        mock_json = {}
        super(BinanceInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_kwargs=kwargs)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = dict()
        super(BinanceInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class BitfinexInterfacTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.bitfinex.Bitfinex._get_supported_pairs',
               return_value=['BTC-USD']):
        exchange = Bitfinex(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
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
        mock_json = bitfinex_ticker
        super(BitfinexInterfacTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = bitfinex_order_book
        super(BitfinexInterfacTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = bitfinex_trades
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

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(BitfinexInterfacTests, self).test_wallet_formatter(expected_result, mock_json)


class BitstampInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.bitstamp.Bitstamp._get_supported_pairs',
               return_value=['BTC-USD']):
        exchange = Bitstamp(key='shadow', secret='panda', user_id='1234')

    @patch('bitex.interface.rest.RESTInterface.request')
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
        mock_json = bitstamp_ticker
        super(BitstampInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = bitstamp_order_book
        super(BitstampInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = bitstamp_trades
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


class BittrexInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.bittrex.Bittrex._get_supported_pairs',
               return_value=['BTC-USD']):
        exchange = Bittrex(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Bittrex(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=True)
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
        mock_json = bittrex_ticker
        super(BittrexInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = bittrex_order_book
        super(BittrexInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = bittrex_trades
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


class CCEXInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.ccex.CCEX._get_supported_pairs',
               return_value=['BTC-USD']):
        exchange = CCEX(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = CCEX(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(ccex_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = CCEX()
        mocked_request_func.assert_called_with('GET', 'https://c-cex.com/t/pairs.json')
        expected_list = sorted(ccex_pairs_parsed['pairs'])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = ccex_ticker
        super(CCEXInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = ccex_order_book
        super(CCEXInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = ccex_trades
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


class CoinCheckInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.coincheck.CoinCheck._get_supported_pairs', return_value=['BTC-USD']):
        exchange = CoinCheck(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = CoinCheck(key='1231', secret='152561')
        api.request('DELETE', 'some_endpoint', authenticate=True)
        mocked_api.assert_called_with('DELETE', 'some_endpoint', authenticate=True)
        api.request('GET','some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)
        self.fail("CoinCheck Employs various HTTP Verbs for private endpoints - these must be "
                  "tested! So far no tests have been written for these, failing..")

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        self.assertEqual(['btc-jpy'], CoinCheck()._get_supported_pairs())

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = coincheck_ticker
        super(CoinCheckInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = coincheck_order_book
        super(CoinCheckInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = coincheck_trades
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


class CryptopiaInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.cryptopia.Cryptopia._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Cryptopia(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
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
        mock_json = cryptopia_tickers
        super(CryptopiaInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = cryptopia_order_book
        super(CryptopiaInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = cryptopia_trades
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


class GDAXInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.gdax.GDAX._get_supported_pairs', return_value=['BTC-USD']):
        exchange = GDAX(key='shadow', secret='panda', passphrase='1234')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = GDAX(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)
        self.fail("GDAX employs various HTTP verbs for private endpoints - these must be "
                  "tested! So far no tests have been written for these, failing..")

    @patch('requests.request', return_value=MockResponse(gdax_products_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = GDAX()
        mocked_request_func.assert_called_with('GET', 'https://api.gdax.com/products')
        expected_list = sorted([d['id'] for d in gdax_products_parsed])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = gdax_ticker
        super(GDAXInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = gdax_order_book
        super(GDAXInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = gdax_trades
        super(GDAXInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GDAXInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GDAXInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GDAXInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(GDAXInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(GDAXInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GDAXInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class GeminiInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.gemini.Gemini._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Gemini(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Gemini(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(gemini_symbols_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Gemini()
        mocked_request_func.assert_called_with('GET', 'https://api.gemini.com/v1/symbols')
        expected_list = sorted([d['symbol'] for d in gemini_symbols_parsed['symbols']])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = gemini_ticker
        super(GeminiInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = gemini_order_book
        super(GeminiInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = gemini_trades
        super(GeminiInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GeminiInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GeminiInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GeminiInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(GeminiInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(GeminiInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(GeminiInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class HitBTCInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.hitbtc.HitBTC._get_supported_pairs', return_value=['BTC-USD']):
        exchange = HitBTC(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = HitBTC(key='1231', secret='152561')
        api.request('some_endpoint', verb='POST', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'public/some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(hitbtc_symbols_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = HitBTC()
        mocked_request_func.assert_called_with('GET', 'https://api.hitbtc.com/api/2/public/symbol')
        expected_list = [entry['id'] for entry in hitbtc_symbols_parsed]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = hitbtc_ticker
        super(HitBTCInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = hitbtc_order_book
        super(HitBTCInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = hitbtc_trades
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


class ItBitInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.itbit.ItBit._get_supported_pairs', return_value=['BTC-USD']):
        exchange = ItBit(key='shadow', secret='panda', user_id='1234')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = ItBit(key='1231', secret='152561')
        api.request('POST', 'some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('GET', 'some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)
        self.fail("GDAX employs various HTTP verbs for private endpoints - these must be "
                  "tested! So far no tests have been written for these, failing..")

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        b = ItBit()
        expected_list = sorted(['XBTUSD', 'XBTSGD', 'XBTEUR'])
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = itbit_ticker
        super(ItBitInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = itbit_order_book
        super(ItBitInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = itbit_trades
        super(ItBitInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(ItBitInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(ItBitInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(ItBitInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(ItBitInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(ItBitInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(ItBitInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class KrakenInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.kraken.Kraken._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Kraken(key='shadow', secret='11LX0lqM9aExe63oe975Fjms5I9plFAPDxj0puwFBKGct79CP9GESjl5IRTDP8bqNaMYWXxEO8UbM0e4kacRtw==')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Kraken(key='1231', secret='11LX0lqM9aExe63oe975Fjms5I9plFAPDxj0puwFBKGct79CP9GESjl5IRTDP8bqNaMYWXxEO8UbM0e4kacRtw==')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'private/some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'public/some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(kraken_asset_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Kraken()
        mocked_request_func.assert_called_with('GET', 'https://api.kraken.com/0/public/AssetPairs')
        expected_list = [pair for pair in kraken_asset_pairs_parsed['result']]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = kraken_ticker
        super(KrakenInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = kraken_order_book
        super(KrakenInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = kraken_trades
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


class OKCoinInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.okcoin.OKCoin._get_supported_pairs', return_value=['BTC-USD']):
        exchange = OKCoin(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
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
        mock_json = okcoin_ticker
        super(OKCoinInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = okcoin_order_book
        super(OKCoinInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = okcoin_trades
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


class PoloniexInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.poloniex.Poloniex._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Poloniex(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Poloniex(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True, params={'command': 'some_endpoint'})
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False, params={'command': 'some_endpoint'})


    @patch('requests.request', return_value=MockResponse(poloniex_tickers_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Poloniex()
        mocked_request_func.assert_called_with('GET', 'https://poloniex.com/public?command=returnTicker')
        expected_list = [pair for pair in poloniex_tickers_parsed]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = poloniex_ticker
        super(PoloniexInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = poloniex_order_book
        super(PoloniexInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = poloniex_trades
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


class QuadrigaCXInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.quadriga.QuadrigaCX._get_supported_pairs', return_value=['BTC-USD']):
        exchange = QuadrigaCX(key='shadow', secret='panda', client_id='1234')

    @patch('bitex.interface.rest.RESTInterface.request')
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
        mock_json = quadriga_ticker
        super(QuadrigaCXInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = quadriga_order_book
        super(QuadrigaCXInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = quadriga_trades
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


class QuoinexInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.quoine.Quoine._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Quoine(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Quoine(key='1231', secret='152561')
        api.request('some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    @patch('requests.request', return_value=MockResponse(quoinex_pairs_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = Quoine()
        mocked_request_func.assert_called_with('GET', 'https://api.quoine.com/products')
        expected_list = sorted({d['currency_pair_code']: d['id'] for d in quoinex_pairs_parsed})
        self.assertEqual(sorted(b.supported_pairs), expected_list)

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = quoinex_ticker
        super(QuoinexInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = quoinex_order_book
        super(QuoinexInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = quoinex_trades
        super(QuoinexInterfaceTests, self).test_trades_formatter(expected_result, mock_json)

    def test_bid_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuoinexInterfaceTests, self).test_bid_formatter(expected_result, mock_json)

    def test_ask_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuoinexInterfaceTests, self).test_ask_formatter(expected_result, mock_json)

    def test_open_orders_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuoinexInterfaceTests, self).test_open_orders_formatter(expected_result, mock_json)

    def test_order_status_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(QuoinexInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_cancel_order_formatter(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(QuoinexInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                                       method_args=additional_args)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(QuoinexInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class TheRockTradingInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.rocktrading.TheRockTrading._get_supported_pairs', return_value=['BTC-USD']):
        exchange = TheRockTrading(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = TheRockTrading(key='1231', secret='152561')
        api.request('POST', 'some_endpoint', authenticate=True)
        mocked_api.assert_called_with('POST', 'some_endpoint', authenticate=True)
        api.request('GET', 'some_endpoint', authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)
        self.fail("TheRockTrading employs various HTTP verbs for private endpoints - these must be "
                  "tested! So far no tests have been written for these, failing..")

    @patch('requests.request', return_value=MockResponse(rock_trading_tickers_parsed, 200))
    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self, mocked_request_func):
        b = TheRockTrading()
        mocked_request_func.assert_called_with('GET', 'https://api.therocktrading.com/v1/funds/tickers')
        expected_list = [t['fund_id'] for t in rock_trading_tickers_parsed['tickers']]
        self.assertEqual(sorted(b.supported_pairs), sorted(expected_list))

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = rock_trading_ticker
        super(TheRockTradingInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = rock_trading_order_book
        super(TheRockTradingInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = rock_trading_trades
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
        additional_kwargs = {'pair': 'BTC-USD'}
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_order_status_formatter(expected_result, mock_json,
                                                            method_kwargs=additional_kwargs)

    def test_cancel_order_formatter(self):
        additional_kwargs = {'pair': 'BTC-USD'}
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_cancel_order_formatter(expected_result, mock_json,
                                                            method_kwargs=additional_kwargs)

    def test_wallet_formatter(self):
        expected_result = tuple()
        mock_json = {}
        super(TheRockTradingInterfaceTests, self).test_wallet_formatter(expected_result, mock_json)


class VaultoroInterfaceTests(BaseInterfaceTests.StandardizedMethodTestCase):
    with patch('bitex.interface.vaultoro.Vaultoro._get_supported_pairs', return_value=['BTC-USD']):
        exchange = Vaultoro(key='shadow', secret='panda')

    @patch('bitex.interface.rest.RESTInterface.request')
    def test_request_generates_params_for_RESTInterface_request_correctly(self, mocked_api):
        api = Vaultoro(key='1231', secret='152561')
        api.request('some_endpoint', post=True, authenticate=True)
        mocked_api.assert_called_with('POST', '1/some_endpoint', authenticate=True)
        api.request('some_endpoint', post=False, authenticate=False)
        mocked_api.assert_called_with('GET', 'some_endpoint', authenticate=False)

    def test_get_supported_pairs_retrieves_data_from_online_endpoint_and_returns_json_content(self):
        b = Vaultoro()
        self.assertEqual(b._get_supported_pairs(), ['BTC-GLD'])

    def test_ticker_formatter(self):
        expected_result = tuple()
        mock_json = vaultoro_ticker
        super(VaultoroInterfaceTests, self).test_ticker_formatter(expected_result, mock_json)

    def test_order_book_formatter(self):
        expected_result = tuple()
        mock_json = vaultoro_order_book
        super(VaultoroInterfaceTests, self).test_order_book_formatter(expected_result, mock_json)

    def test_trades_formatter(self):
        expected_result = tuple()
        mock_json = vaultoro_trades
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
