# Import Built-Ins
import logging
import unittest
import time
import json

# Import Third-Party

# Import Homebrew
from bitex.pairs import BTCUSD, ETHBTC, LTCBTC, ETHUSD
from bitex.interface import Interface, RESTInterface
from bitex.interface import Bitfinex, Bitstamp, Bittrex, BTCE, Bter, CCEX
from bitex.interface import CoinCheck, Cryptopia, HitBTC, Kraken, OKCoin
from bitex.interface import Poloniex, QuadrigaCX, TheRockTrading, Vaultoro
from bitex.exceptions import UnsupportedEndpointError

# Init Logging Facilities
log = logging.getLogger(__name__)

tests_folder_dir = '/home/nils/git/bitex/tests'


class InterfaceTests(unittest.TestCase):
    def test_init_raises_NotImplementedError_for_basic_interface(self):
        iface = Interface(name='CoinCheck', rest_api=None)
        self.assertIs(iface.supported_pairs, None)

        # Assert that the supported_pairs attribute cannot be set
        with self.assertRaises(AttributeError):
            iface.supported_pairs = ['Hello']

        # Assert that is_supported() method evaluates as expected. To test this,
        # circumvent overwrite protection of supported_pairs attribute.
        iface._supported_pairs = ['BTCUSD', 'LTCBTC']

        self.assertTrue(iface.is_supported('BTCUSD'))
        self.assertTrue(iface.is_supported(BTCUSD))
        self.assertTrue(iface.is_supported('LTCBTC'))
        self.assertFalse(iface.is_supported('LTCUSD'))

        # Assert that, by default, _get_supported_pairs() raises a
        # NotImplementedError
        with self.assertRaises(NotImplementedError):
            iface._get_supported_pairs()


class RESTInterfaceTests(unittest.TestCase):
    def test_that_all_methods_raise_not_implemented_errors(self):
        riface = RESTInterface('Test', None)
        funcs = [riface.ticker, riface.order_book, riface.trades,
                 riface.order_status, riface.open_orders, riface.cancel_order,
                 riface.ask, riface.bid]
        for f in funcs:
            # Pass three Nones, since the max expected number of args is 3, and
            # arguments are unimportant in this test's context.
            with self.assertRaises(NotImplementedError, msg=f.__name__):
                f(None, None, None)


class BitfinexInterfacTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Bitfinex()
        resp = api.ticker(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for k in ['mid', 'bid', 'ask', 'last_price', 'low', 'high', 'volume', 'timestamp']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))
        # Assert that this method works on v2 as well
        api = Bitfinex(version='v2')
        try:
            api.ticker(BTCUSD)
        except UnsupportedEndpointError:
            self.fail('Version 2 not supported!')

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Bitfinex()
        resp = api.order_book(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())
            for d in resp.json()[side]:
                for k in ['price', 'amount', 'timestamp']:
                    self.assertIn(k, d, msg=(k, d, side, resp.json()))
        # Assert that this method works on v2 as well
        api = Bitfinex(version='v2')
        try:
            api.order_book(BTCUSD)
        except UnsupportedEndpointError:
            self.fail('Version 2 not supported!')

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Bitfinex()
        resp = api.trades(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for d in resp.json():
            for k in ['timestamp', 'tid', 'price', 'amount', 'exchange', 'type']:
                self.assertIn(k, d, msg=(k, d, resp.json()))
        # Assert that this method works on v2 as well
        api = Bitfinex(version='v2')
        try:
            api.trades(BTCUSD)
        except UnsupportedEndpointError:
            self.fail('Version 2 not supported!')

    def test_and_validate_data_for_stats_endpoint_method_working_correctly(self):
        api = Bitfinex()
        resp = api.stats(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for d in resp.json():
            for k in ['period', 'volume']:
                self.assertIn(k, d, msg=(k, d, resp.json()))
        # Assert that this method works on v2 as well
        api = Bitfinex(version='v2')
        try:
            api.stats(BTCUSD, key='funding.size', size='1m', side='long',
                      section='last')
        except UnsupportedEndpointError:
            self.fail('Version 2 not supported!')

    def test_and_validate_data_for_lends_endpoint_method_working_correctly(self):
        api = Bitfinex()
        resp = api.lends('BTC')
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for d in resp.json():
            for k in ['rate', 'amount_lent', 'amount_used', 'timestamp']:
                self.assertIn(k, d, msg=(k, d, resp.json()))
        # Assert that an error is raised if the API version isn't v1
        api = Bitfinex(version='v2')
        with self.assertRaises(UnsupportedEndpointError):
            api.lends('BTC')

    def test_and_validate_data_for_funding_book_endpoint_method_working_correctly(self):
        api = Bitfinex()
        resp = api.funding_book('BTC')
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that we have bids and asks, and that their entries are in the
        # expected format
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())
            for d in resp.json()[side]:
                for k in ['rate', 'amount', 'period', 'timestamp', 'frr']:
                    self.assertIn(k, d, msg=(k, d, side, resp.json()))
        # Assert that an error is raised if the API version isn't v1
        api = Bitfinex(version='v2')
        with self.assertRaises(UnsupportedEndpointError):
            api.funding_book('BTC')

    def test_and_validate_data_for_symbols_endpoint_method_working_correctly(self):
        api = Bitfinex()
        # Assert that Bitfinex().symbols() returns a list
        resp = api.symbols()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list)
        # Assert that if verbose=True is passed, symbols returns dicts
        resp = api.symbols(verbose=True)
        for d in resp.json():
            for k in ['pair', 'price_precision', 'initial_margin', 'minimum_margin',
                      'maximum_order_size', 'minimum_order_size', 'expiration']:
                self.assertIn(k, d, msg=(k, d, resp.json()))
        # Assert that an error is raised if the API version isn't v1
        api = Bitfinex(version='v2')
        with self.assertRaises(UnsupportedEndpointError):
            api.symbols()
        with self.assertRaises(UnsupportedEndpointError):
            api.symbols(verbose=True)

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Bitfinex(config='%s/auth/bitfinex.ini' % tests_folder_dir)
        # Assert that Bitfinex().wallet() returns a list of dicts with expected
        # keys
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list)
        for d in resp.json():
            for k in ['type', 'currency', 'amount', 'available']:
                self.assertIn(k, d, msg=(k, d, resp.json()))
        # Assert that an error is raised if the API version isn't v1
        api = Bitfinex(config='%s/auth/bitfinex.ini' % tests_folder_dir)
        api.REST.version = 'v2'
        with self.assertRaises(UnsupportedEndpointError):
            api.wallet()

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Bitfinex(config='%s/auth/bitfinex.ini' % tests_folder_dir)
        # Assert that Bitfinex().wallet() returns a list of dicts with expected
        # keys
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list)
        if resp.json():
            for d in resp.json():
                for k in ['id', 'symbol', 'exchange', 'price', 'timestamp',
                          'is_alive', 'is_cancelled', 'is_hidden', 'was_forced',
                          'original_amount', 'remaining_amount', 'executed_amount',
                          'avg_execution_price', 'side', 'type']:
                    self.assertIn(k, d, msg=(k, d, resp.json()))
        # Assert that an error is raised if the API version isn't v1
        api = Bitfinex(config='%s/auth/bitfinex.ini' % tests_folder_dir)
        api.REST.version = 'v2'
        with self.assertRaises(UnsupportedEndpointError):
            api.open_orders()


class BitstampInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Bitstamp()
        resp = api.ticker(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for k in ['last', 'bid', 'ask', 'vwap', 'low', 'high', 'volume',
                  'open', 'timestamp']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Bitstamp()
        resp = api.order_book(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())
            for l in resp.json()[side]:
                self.assertIsInstance(l, list, msg=(l, side, resp.json()))
                self.assertEqual(len(l), 2, msg=(l, side, resp.json()))

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Bitstamp()
        resp = api.trades(BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        # Assert that data is in expected format
        for d in resp.json():
            for k in ['date', 'tid', 'price', 'amount', 'type']:
                self.assertIn(k, d, msg=(k, d, resp.json()))

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Bitstamp(config='%s/auth/bitstamp.ini' % tests_folder_dir)
        # Assert that Bitstamp().wallet(pair=BTCUSD) returns a list of dicts with expected
        # keys
        resp = api.wallet(pair=BTCUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict)
        for k in resp.json():
            self.assertIn(k, ['usd_reserved', 'usd_balance', 'usd_available',
                              'btc_balance', 'btc_reserved', 'btc_available',
                              'fee'], msg=(resp.request.url, resp.json()))

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict)
        currencies = ['ltc', 'btc', 'xrp', 'usd', 'eur']
        suffixes = ['balance', 'reserved', 'available']
        keys = ['btcusd_fee', 'btceur_fee', 'eurusd_fee',
                'xrpusd_fee', 'xrpeur_fee', 'xrpbtc_fee',
                'ltceur_fee', 'ltcusd_fee', 'ltcbtc_fee']
        for cur in currencies:
            for suffix in suffixes:
                keys.append(cur + '_' + suffix)
        for k in resp.json():
            self.assertIn(k, keys)

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Bitstamp(config='%s/auth/bitstamp.ini' % tests_folder_dir)
        # Assert that Bitstamp().open_orders() returns a list of dicts with expected
        # keys
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list)
        if resp.json():
            for d in resp.json():
                for k in ['id', 'currency_pair', 'price', 'datetime',
                          'amount', 'side', 'type']:
                    self.assertIn(k, d, msg=(k, d, resp.json()))


class BittrexInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Bittrex()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        # Assert that data is in expected format
        for k in ['Last', 'Bid', 'Ask', 'High', 'Low', 'MarketName', 'Created',
                  'Volume', 'BaseVolume', 'TimeStamp', 'OpenBuyOrders',
                  'OpenSellOrders', 'PrevDay']:
            self.assertIn(k, resp.json()['result'][0], msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Bittrex()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        # Assert that data is in expected format
        result = resp.json()['result']
        for side in ('buy', 'sell'):
            self.assertIn(side, result)

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Bittrex()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        # Assert that data is in expected format
        for d in resp.json()['result']:
            for k in ['Id', 'TimeStamp', 'Price', 'Quantity', 'OrderType',
                      'FillType', 'Total']:
                self.assertIn(k, d, msg=(k, d, resp.json()))

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Bittrex(config='%s/auth/bittrex.ini' % tests_folder_dir)
        # Assert that Bittrex().wallet(currency=BTC) returns a dict with expected
        # keys
        resp = api.wallet('BTC')
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=(resp.json(), resp.request.url))
        self.assertIsInstance(resp.json(), dict)
        for k in resp.json()['result']:
            self.assertIn(k, ['Currency', 'Balance', 'Available', 'Pending',
                              'CryptoAddress', 'Requested', 'Uuid'],
                          msg=(resp.request.url, resp.json()))

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        self.assertIsInstance(resp.json()['result'], list)
        for d in resp.json()['result']:
            for k in d:
                self.assertIn(k, ['Currency', 'Balance', 'Available', 'Pending',
                                  'CryptoAddress', 'Requested', 'Uuid'],
                              msg=(d, k, resp.json()))

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Bittrex(config='%s/auth/bittrex.ini' % tests_folder_dir)
        # Assert that Bittrex().open_orders() returns a list of dicts with expected
        # keys
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        for d in resp.json()['result']:
            for k in ['Uuid', 'OrderUuid', 'Exchange', 'OrderType', 'Quantity',
                      'QuantityRemaining', 'Limit', 'CommissionPaid', 'Price',
                      'PricePerUnit', 'Opened', 'Closed', 'CancelInitiated',
                      'ImmediateOrCancel', 'IsConditional', 'Condition',
                      'ConditionTarget']:
                self.assertIn(k, d, msg=(k, d, resp.json()))


class BTCEInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = BTCE()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        data = resp.json()[ETHBTC.format_for('BTC-E')]
        # Assert that data is in expected format
        for k in ['last', 'buy', 'sell', 'high', 'low', 'vol_cur', 'avg',
                  'updated', 'vol']:
            self.assertIn(k, data, msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = BTCE()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())

        # Assert that data is in expected format
        result = resp.json()[ETHBTC.format_for('BTC-E')]
        for side in ('bids', 'asks'):
            self.assertIn(side, result)

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = BTCE()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())

        data = resp.json()[ETHBTC.format_for('BTC-E')]
        # Assert that data is in expected format
        for d in data:
            self.assertIsInstance(d, dict)

    # Test Private Endpoints

    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = BTCE(config='%s/auth/btce.ini' % tests_folder_dir)

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertEqual(resp.json()['success'], 1, msg=resp.json())
        self.assertIn('return', resp.json(), msg=resp.json())
        data = resp.json()['return']
        self.assertIn('funds', data)

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = BTCE(config='%s/auth/btce.ini' % tests_folder_dir)
        # Assert that Bittrex().open_orders() returns a list of dicts with expected
        # keys
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertEqual(resp.json()['success'], 1, msg=resp.json())


class BterInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Bter()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['result'])
        # Assert that data is in expected format
        for k in ['last', 'lowestAsk', 'highestBid', 'percentChange',
                  'baseVolume', 'quoteVolume', 'high24hr', 'low24hr']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Bter()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())

        # Assert that data is in expected format

        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())

    @unittest.expectedFailure
    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Bter()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        try:
            self.assertEqual(resp.json()['result'], msg=resp.request.url)
        except KeyError:
            self.fail("Trades endpoint returns empty page!")
        data = resp.json()['data']
        # Assert that data is in expected format
        for d in data:
            self.assertIsInstance(d, dict)

    # Test Private Endpoints

    @unittest.expectedFailure
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Bter(config='%s/auth/bter.ini' % tests_folder_dir)

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['result'], msg=resp.json())
        self.assertIn('available', resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Bter(config='%s/auth/bter.ini' % tests_folder_dir)
        # Assert that Bittrex().open_orders() returns a list of dicts with expected
        # keys
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['result'], msg=resp.json())


class CCEXInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = CCEX()
        resp = api.ticker(LTCBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.text)
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        # Assert that data is in expected format
        self.assertIn('ticker', resp.json())

        for k in ['lastbuy', 'lastsell', 'low', 'high', 'avg',
                  'buy', 'sell', 'lastprice', 'buysupport', 'updated']:
            self.assertIn(k, resp.json()['ticker'], msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = CCEX()
        resp = api.order_book(LTCBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        # Assert that data is in expected format
        data = resp.json()['result']
        # Assert that data is in expected format
        for side in ('buy', 'sell'):
            self.assertIn(side, data)

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = CCEX()
        resp = api.trades(LTCBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        for item in resp.json()['result']:
            self.assertIsInstance(item, dict, msg=(item, resp.json()))

    # Test Private Endpoints

    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = CCEX(config='%s/auth/ccex.ini' % tests_folder_dir)
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.request.url)
        self.assertTrue(resp.json()['success'], msg=resp.json())

        for item in resp.json()['result']:
            self.assertIsInstance(item, dict, msg=(item, resp.json()))

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = CCEX(config='%s/auth/ccex.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        for item in resp.json()['result']:
            self.assertIsInstance(item, dict, msg=(item, resp.json()))


class CoinCheckInterfaceTests(unittest.TestCase):
    def tearDown(self):
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = CoinCheck()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        for k in ['last', 'low', 'high', 'bid', 'ask', 'volume', 'timestamp']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = CoinCheck()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list, msg=resp.json())
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json(), msg=resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = CoinCheck()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list, msg=resp.json())
        for d in resp.json():
            self.assertIsInstance(d, dict)

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = CoinCheck(config='%s/auth/coincheck.ini' % tests_folder_dir)
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = CoinCheck(config='%s/auth/coincheck.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['success'], msg=resp.json())
        self.assertIn('orders', resp.json(), msg=resp.json())
        for order in resp.json()['orders']:
            self.assertIsInstance(order, dict, msg=(order, resp.json()))


class CryptopiaInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Cryptopia()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['Success'], msg=resp.json())
        for k in ['AskPrice', 'BidPrice', 'High', 'Low',
                  'Volume', 'LastPrice', 'BuyVolume', 'SellVolume', 'Change',
                  'Open', 'Close', 'BaseVolume', 'BaseBuyVolume', 
                  'BaseSellVolume', 'TradePairId', 'Label']:
            self.assertIn(k, resp.json()['Data'], msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Cryptopia()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['Success'], msg=resp.json())
        self.assertIn('Data', resp.json(), msg=resp.json())
        for side in ('Buy', 'Sell'):
            self.assertIn(side, resp.json()['Data'], msg=resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Cryptopia()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['Success'], msg=resp.json())
        self.assertIn('Data', resp.json(), msg=resp.json())
        for d in resp.json()['Data']:
            self.assertIsInstance(d, dict)

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Cryptopia(config='%s/auth/cryptopia.ini' % tests_folder_dir)
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['Success'], msg=resp.json())
        self.assertIn('Data', resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Cryptopia(config='%s/auth/cryptopia.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['Success'], msg=resp.json())
        self.assertIn('Data', resp.json())


class HitBTCInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = HitBTC()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        # Assert that data is in expected format
        for k in ['last', 'bid', 'ask', 'high', 'low', 'volume', 'open',
                  'volume_quote', 'timestamp']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = HitBTC()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = HitBTC()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        self.assertIn('trades', resp.json())

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = HitBTC(config='%s/auth/hitbtc.ini' % tests_folder_dir)
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.request.url)
        self.assertIn('balance', resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = HitBTC(config='%s/auth/hitbtc.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        self.assertIn('orders', resp.json())


class KrakenInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Kraken()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertFalse(resp.json()['error'], msg=resp.json())
        pair = ETHBTC.format_for('Kraken')
        self.assertIn(pair, resp.json()['result'], msg=resp.json())
        for k in 'a,b,c,v,p,t,l,h,o'.split(','):
            self.assertIn(k, resp.json()['result'][pair], msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Kraken()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertFalse(resp.json()['error'], msg=resp.json())
        pair = ETHBTC.format_for('Kraken')
        self.assertIn(pair, resp.json()['result'], msg=resp.json())

        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json()['result'][pair])

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Kraken()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertFalse(resp.json()['error'], msg=resp.json())
        pair = ETHBTC.format_for('Kraken')
        self.assertIn(pair, resp.json()['result'], msg=resp.json())
        data = resp.json()['result'][pair]
        self.assertIsInstance(data, list)
        for d in data:
            self.assertIsInstance(d, list)

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Kraken(config='%s/auth/kraken.ini' % tests_folder_dir)

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertFalse(resp.json()['error'], msg=resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Kraken(config='%s/auth/kraken.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertFalse(resp.json()['error'], msg=resp.json())


class OKCoinInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = OKCoin()
        resp = api.ticker(ETHUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIn('ticker', resp.json())
        for k in ('buy', 'high', 'low', 'sell', 'vol'):
            self.assertIn(k, resp.json()['ticker'], msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = OKCoin()
        resp = api.order_book(ETHUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIn('asks', resp.json())
        self.assertIn('bids', resp.json())
        for b, a in zip(resp.json()['bids'], resp.json()['asks']):
            self.assertIsInstance(b, list)
            self.assertIsInstance(a, list)

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = OKCoin()
        resp = api.trades(ETHUSD)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list)
        for d in resp.json():
            self.assertIsInstance(d, dict)
            for k in ('date', 'date_ms', 'price', 'amount', 'tid', 'type'):
                self.assertIn(k, d)

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = OKCoin(config='%s/auth/okcoin.ini' % tests_folder_dir)
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['result'], msg=resp.json())
        self.assertIn('info', resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = OKCoin(config='%s/auth/okcoin.ini' % tests_folder_dir)
        resp = api.open_orders(symbol=ETHUSD.format_for('OKCoin'))
        self.assertEqual(resp.status_code, 200, msg=resp.request.url)
        self.assertTrue(resp.json()['result'], msg=resp.json())
        self.assertIn('orders', resp.json())
        self.assertIsInstance(resp.json()['orders'], list)


class PoloniexInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Poloniex()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=(resp.text, resp.request.url))
        self.assertIsInstance(resp.json(), dict, msg=(resp.json()))
        pair = ETHBTC.format_for('Poloniex')
        self.assertIn(pair, resp.json(), msg=resp.json())

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Poloniex()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        self.assertIn('seq', resp.json(), msg=resp.json())
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Poloniex()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list, msg=resp.json())
        for d in resp.json():
            self.assertIsInstance(d, dict, msg=resp.json())

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Poloniex(config='%s/auth/poloniex.ini' % tests_folder_dir)

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Poloniex(config='%s/auth/poloniex.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=(resp.json(), resp.request.url))
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        for key in resp.json():
            self.assertIsInstance(resp.json()[key], list, msg=resp.json())
            for l in resp.json()[key]:
                self.assertIsInstance(l, list, msg=(l, key, resp.json()))


class QuadrigaCXInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = QuadrigaCX()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertNotIn('error', resp.json())
        for k in ['high', 'low', 'last', 'vwap', 'volume', 'bid', 'ask']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = QuadrigaCX()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        self.assertNotIn('error', resp.json())
        for key in ('bids', 'asks', 'timestamp'):
            self.assertIn(key, resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = QuadrigaCX()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list, msg=resp.json())
        self.assertNotIn('error', resp.json())
        for item in resp.json():
            self.assertIsInstance(item, dict, msg=resp.json())

    # Test Private Endpoints
    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = QuadrigaCX(config='%s/auth/quadrigacx.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertNotIn('error', resp.json())
        try:
            self.assertIsInstance(resp.json(), dict, msg=resp.json())
        except AssertionError:
            # This may be due to empty wallets being None, and the result
            # may be instead an empty list. Assert this.
            self.assertIsInstance(resp.json(), list, msg=resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = QuadrigaCX(config='%s/auth/quadrigacx.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), list, msg=resp.json())
        self.assertNotIn('error', resp.json())


class TheRockTradingInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = TheRockTrading()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        self.assertNotIn('errors', resp.json(), msg=resp.json())
        # Assert that data is in expected format
        for k in ['last', 'high', 'low', 'open', 'close', 'fund_id',
                  'bid', 'ask', 'date', 'volume', 'volume_traded']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = TheRockTrading()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertIsInstance(resp.json(), dict, msg=resp.json())
        self.assertNotIn('errors', resp.json(), msg=resp.json())
        for k in ('bids', 'asks', 'fund_id', 'date'):
            self.assertIn(k, resp.json(), msg=resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = TheRockTrading()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertNotIn('errors', resp.json(), msg=resp.json())
        self.assertIn('trades', resp.json(), msg=resp.json())

    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = TheRockTrading(config='%s/auth/rocktrading.ini' % tests_folder_dir)

        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertNotIn('errors', resp.json(), msg=resp.json())
        self.assertIn('balances', resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = TheRockTrading(config='%s/auth/rocktrading.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertNotIn('errors', resp.json(), msg=resp.json())
        self.assertIn('orders', resp.json())


class VaultoroInterfaceTests(unittest.TestCase):
    def tearDown(self):
        # Wait one second to reduce load on API
        time.sleep(1)

    # PUBLIC ENDPOINT TESTS
    def test_and_validate_data_for_ticker_endpoint_method_working_correctly(self):
        api = Vaultoro()
        resp = api.ticker(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertTrue(resp.json()['result'])
        # Assert that data is in expected format
        for k in ['last', 'lowestAsk', 'highestBid', 'percentChange',
                  'baseVolume', 'quoteVolume', 'high24hr', 'low24hr']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Vaultoro()
        resp = api.order_book(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())

        # Assert that data is in expected format

        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Vaultoro()
        resp = api.trades(ETHBTC)
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        try:
            self.assertEqual(resp.json()['result'], msg=resp.request.url)
        except KeyError:
            self.fail("Trades endpoint returns empty page!")
        data = resp.json()['data']
        # Assert that data is in expected format
        for d in data:
            self.assertIsInstance(d, dict)

    def test_and_validate_data_for_wallet_endpoint_method_working_correctly(self):
        api = Vaultoro(config='%s/auth/vaultoro.ini' % tests_folder_dir)

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200, msg=resp.json())
        self.assertEqual(resp.json()['status'], 'success', msg=resp.json())
        self.assertIn('data', resp.json())

    def test_and_validate_data_for_open_orders_endpoint_method_working_correctly(self):
        api = Vaultoro(config='%s/auth/bter.ini' % tests_folder_dir)
        resp = api.open_orders()
        self.assertEqual(resp.json()['status'], 'success', msg=resp.json())
        self.assertIn('data', resp.json())

if __name__ == '__main__':
    unittest.main(verbosity=2)
