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
from bitex.http import KrakenHTTP

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