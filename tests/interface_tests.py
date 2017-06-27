# Import Built-Ins
import logging
import unittest
import time

# Import Third-Party

# Import Homebrew
from bitex.pairs import BTCUSD
from bitex.interface import Interface, RESTInterface, Bitfinex, Bitstamp
from bitex.exceptions import UnsupportedPairError, EmptySupportedPairListWarning
from bitex.exceptions import UnsupportedEndpointError

# Init Logging Facilities
log = logging.getLogger(__name__)

tests_folder_dir = '/home/nls/git/bitex/tests'

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
        self.assertEqual(resp.status_code, 200)
        # Assert that data is in expected format
        for k in ['last', 'bid', 'ask', 'vwap', 'low', 'high', 'volume',
                  'open', 'timestamp']:
            self.assertIn(k, resp.json(), msg=(k, resp.json()))

    def test_and_validate_data_for_order_book_endpoint_method_working_correctly(self):
        api = Bitstamp()
        resp = api.order_book(BTCUSD)
        self.assertEqual(resp.status_code, 200)
        # Assert that data is in expected format
        for side in ('bids', 'asks'):
            self.assertIn(side, resp.json())
            for l in resp.json()[side]:
                self.assertIsInstance(l, list, msg=(l, side, resp.json()))
                self.assertEqual(len(l), 2, msg=(l, side, resp.json()))

    def test_and_validate_data_for_trades_endpoint_method_working_correctly(self):
        api = Bitstamp()
        resp = api.trades(BTCUSD)
        self.assertEqual(resp.status_code, 200)
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
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), dict)
        for k in resp.json():
            self.assertIn(k, ['usd_reserved', 'usd_balance', 'usd_available',
                              'btc_balance', 'btc_reserved', 'btc_available',
                              'fee'], msg=(resp.request.url, resp.json()))

        # Assert that if no pair is passed, we get a snapshot of all wallets:
        resp = api.wallet()
        self.assertEqual(resp.status_code, 200)
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
