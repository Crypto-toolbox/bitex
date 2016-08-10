"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging
import unittest
import requests
# Import Third-Party

# Import Homebrew
from bitex.http import KrakenHTTP, BitstampHTTP, BitfinexHTTP

log = logging.getLogger(__name__)

class KrakenHTTPTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_returns_request_object(self):
        k = KrakenHTTP(key_file="")
        # Returns a response object
        r = k.server_time()
        self.assertIsInstance(r, requests.models.Response)
        self.assertEqual(r.status_code, 200)
        # .json() contains 'result' and 'error' keys in dict
        self.assertIn('result', r.json())
        self.assertIn('error', r.json())

    def test_can_connect_to_public_endpoints(self):
        k = KrakenHTTP(key_file="")

        # connect to ticker endpoint and 'error' is empty
        r = k.ticker('XBTEUR')
        self.assertFalse(r.json()['error'])
        self.assertIn('a', r.json()['result']['XXBTZEUR'])
        self.assertIn('b', r.json()['result']['XXBTZEUR'])
        self.assertIn('v', r.json()['result']['XXBTZEUR'])

        # connect to trades endpoint and 'error' is empty
        r = k.trades('XBTEUR')
        self.assertFalse(r.json()['error'])
        self.assertIsInstance(r.json()['result']['XXBTZEUR'], list)

        # connect to orderbook endpoint and 'error' is empty
        r = k.order_book('XBTEUR')
        self.assertFalse(r.json()['error'])
        self.assertIn('asks', r.json()['result']['XXBTZEUR'])
        self.assertIn('bids', r.json()['result']['XXBTZEUR'])

    def test_client_loads_key_and_secret_correctly(self):
        # Load by passing args
        k = KrakenHTTP(key='This_is_a_key', secret='This_is_a_secret')
        self.assertTrue(k._api.key == 'This_is_a_key')
        self.assertTrue(k._api.secret == 'This_is_a_secret')

        # load by using key file
        k = KrakenHTTP(key_file="./test.key")
        self.assertTrue(k._api.key == 'This_is_a_key')
        self.assertTrue(k._api.secret == 'This_is_a_secret')

    def test_can_connect_to_private_endpoint(self):
        # connect to balance endpoint
        # connect to orders endpoint
        # connect to ledger endpoint
        # connect to add_order endpoint
        # connect to cancel_order endpoint
        # connect to fees endpoint
        pass

class BitstampHTTPTest(unittest.TestCase):
    def test_public_endpoints_return_requests_response_object(self):
        k = BitstampHTTP()
        # Returns a response object
        r = k.ticker('BTCUSD')
        self.assertIsInstance(r, requests.models.Response)
        r = k.trades('BTCUSD')
        self.assertIsInstance(r, requests.models.Response)
        r = k.order_book('BTCUSD')
        self.assertIsInstance(r, requests.models.Response)

    def test_private_endpoints_returns_requests_response_object(self):
        k = BitstampHTTP()
        # Returns a response object with a status code
        r = k.balance()
        self.assertIsInstance(r, requests.models.Response)
        r = k.orders()
        self.assertIsInstance(r, requests.models.Response)
        r = k.ledger()
        self.assertIsInstance(r, requests.models.Response)
        r = k.add_order(200.0, 1, 'btcusd', 'ask')
        self.assertIsInstance(r, requests.models.Response)
        r = k.cancel_order(11111111)
        self.assertIsInstance(r, requests.models.Response)
        r = k.fees()
        self.assertIsInstance(r, requests.models.Response)

    def test_order_book(self):
        k = BitstampHTTP()
        r = k.order_book('btcusd')
        # Must return a dict
        self.assertIsInstance(r.json(), dict)

        # Must contain certain keys
        a = {'asks', 'bids', 'timestamp'}
        b = set(r.json().keys())
        print(a,b)
        self.assertCountEqual(a, b)

    def test_ticker(self):
        k = BitstampHTTP()
        r = k.ticker('btcusd')
        # Must return a dict
        self.assertIsInstance(r.json(), dict)

        # Must contain certain keys
        a = {'last', 'high', 'low', 'vwap', 'volume', 'bid', 'ask', 'open', 'timestamp'}
        b = set(r.json().keys())
        self.assertCountEqual(a, b)

    def test_trades(self):
        k = BitstampHTTP()
        r = k.trades('btcusd')
        # Must return a list
        self.assertIsInstance(r.json(), list)

        # list must contain dict only, with certain keys
        a = {'date', 'tid', 'price', 'amount', 'type'}
        for b in r.json():
            self.assertIsInstance(b, dict)
            self.assertCountEqual(a, set(b.keys()))


class BitfinexHTTPTest(unittest.TestCase):
    def test_public_endpoints_return_requests_response_object(self):
        k = BitfinexHTTP()
        # Returns a response object
        r = k.ticker('BTCUSD')
        self.assertIsInstance(r, requests.models.Response)
        r = k.trades('BTCUSD')
        self.assertIsInstance(r, requests.models.Response)
        r = k.order_book('BTCUSD')
        self.assertIsInstance(r, requests.models.Response)

    def test_private_endpoints_returns_requests_response_object(self):
        k = BitfinexHTTP()
        # Returns a response object with a status code
        r = k.balance()
        self.assertIsInstance(r, requests.models.Response)
        r = k.orders()
        self.assertIsInstance(r, requests.models.Response)
        r = k.ledger()
        self.assertIsInstance(r, requests.models.Response)
        r = k.add_order(200.0, 1, 'btcusd', 'ask')
        self.assertIsInstance(r, requests.models.Response)
        r = k.cancel_order(11111111)
        self.assertIsInstance(r, requests.models.Response)
        r = k.fees()
        self.assertIsInstance(r, requests.models.Response)

    def test_order_book(self):
        k = BitfinexHTTP()
        r = k.order_book('btcusd')
        # Must return a dict
        self.assertIsInstance(r.json(), dict)

        # Must contain certain keys
        a = {'asks', 'bids'}
        b = set(r.json().keys())
        self.assertCountEqual(a, b)

    def test_ticker(self):
        k = BitfinexHTTP()
        r = k.ticker('btcusd')
        # Must return a dict
        self.assertIsInstance(r.json(), dict)

        # Must contain certain keys
        a = {'last_price', 'high', 'low', 'volume', 'bid', 'ask', 'mid',
             'timestamp'}
        b = set(r.json().keys())
        self.assertCountEqual(a, b)

    def test_trades(self):
        k = BitfinexHTTP()
        r = k.trades('btcusd')
        # Must return a list
        self.assertIsInstance(r.json(), list)

        # list must contain dict only, with certain keys
        a = {'created_at', 'id', 'pair', 'price', 'amount', 'side', 'platform'}
        for b in r.json():
            self.assertIsInstance(b, dict)
            self.assertCountEqual(a, set(b.keys()))
