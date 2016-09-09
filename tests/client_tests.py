"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging
import unittest
import requests
import json
# Import Third-Party

# Import Homebrew
from bitex.api.api import RESTAPI
from bitex.api.rest import KrakenREST, CryptopiaREST, CCEXRest, GeminiREST
from bitex.api.rest import YunbiREST, RockTradingREST

log = logging.getLogger(__name__)


class APITests(unittest.TestCase):
    """
    Tests APIs for connection establishment, authentication, key loading.
    """
    def setUp(self):
        self.api = RESTAPI('http://google.com/api', api_version='v1', key='12345',
                           secret='abcde')

    def tearDown(self):
        self.api = None

    def test_restapi_load_key(self):
        self.api.load_key("test.key")
        self.assertTrue(self.api.secret, "This_is_a_secret")
        self.assertTrue(self.api.key, "This_is_a_key")

    def test_restapi_nonce(self):
        n = self.api.nonce()
        self.assertTrue(n.strip().isdigit())

    def test_restapi_query(self):
        # Test that the unathenticated request is built correctly
        r = self.api.query('testing/endpoint/', authenticate=False,
                       request_method=requests.get,
                       params={'test_param': "chimichanga"})
        url = 'http://google.com/api/v1/testing/endpoint/?test_param=chimichanga'
        self.assertTrue(r.request.url == url)

        # Test that authentication requests are built correctly
        r = self.api.query('testing/endpoint/', authenticate=True,
                       request_method=requests.get,
                       params={'test_param': "chimichanga"})
        url = 'http://google.com/api/v1/testing/endpoint/?test_param=authenticated_chimichanga'
        self.assertTrue(r.request.url == url)

    def test_sign_returns_tuple_of_str_and_dict(self):
        r = self.api.sign()
        self.assertIsInstance(r, tuple)
        self.assertIsInstance(r[0], str)
        self.assertIsInstance(r[1], dict)


class KrakenAPITest(APITests):
    def setUp(self):
        self.api = KrakenREST()
        self.api.load_key('kraken.key')

    def test_public_query(self):
        # query() returns a valid requests.Response object
        r = self.api.query('GET', 'Time')
        self.assertIsInstance(r, requests.Response)

        # query() is succesful (No errors)
        self.assertTrue(r.json()['error'] == [],
                        "Error in Response: %s" % r.json()['error'])

    def test_private_query(self):
        # API Key and secret are loaded?
        self.assertTrue(self.api.key, 'API Key is empty!')
        self.assertTrue(self.api.secret, 'Secret Key is empty!')

        # query() returns a valid request object
        r = self.api.query('POST', 'private/OpenOrders', authenticate=True)
        self.assertIsInstance(r, requests.Response)

        # query() with flag authenticate=True builds valid signature (No errors)
        self.assertTrue(r.json()['error'] == [],
                        "Error in Response: %s" % r.json()['error'])


class CryptopiaAPITest(APITests):
    def setUp(self):
        self.api = CryptopiaREST()

    def test_public_query(self):
        # query() returns a valid requests.Response object
        r = self.api.query('GET', 'GetMarketOrders/101')
        self.assertIsInstance(r, requests.Response)

        # query() is succesful (No errors)
        self.assertTrue(r.json()['Success'],
                        "Error in Response: %s" % r.request.url)

    def test_private_query(self):
        pass


class CCEXAPITest(APITests):
    def setUp(self):
        self.api = CCEXRest()

    def test_public_query(self):
        # query() returns a valid requests.Response object
        r = self.api.query('GET', 'api_pub.html?a=getorderbook',
                           params={'market': 'ltc-btc', 'type': 'both'})
        self.assertIsInstance(r, requests.Response)

        # query() is succesful (No errors)
        self.assertTrue(r.json()['success'],
                        "Error in Response: %s" % r.request.url)

    def test_private_query(self):
        pass


class GeminiAPITest(APITests):
    def setUp(self):
        self.api = GeminiREST()

    def test_public_query(self):
        # query() returns a valid requests.Response object
        r = self.api.query('GET', 'book/ETHBTC')
        self.assertIsInstance(r, requests.Response)

        # query() is succesful (No error message)
        self.assertNotIn('message', r.json(), "Error in Response: %s" % r.request.url)

    def test_private_query(self):
        pass


class YunbiAPITest(APITests):
    def setUp(self):
        self.api = YunbiREST()

    def test_public_query(self):
        # query() returns a valid requests.Response object
        r = self.api.query('GET', 'markets.json')
        self.assertIsInstance(r, requests.Response)

        # query() is succesful (No error message)
        self.assertNotIn('message', r.json())

    def test_private_query(self):
        pass


class TheRockTradingAPITest(APITests):
    def setUp(self):
        self.api = RockTradingREST()

    def test_public_query(self):
        # query() returns a valid requests.Response object
        r = self.api.query('GET', 'funds/BTCEUR/orderbook')
        self.assertIsInstance(r, requests.Response)

        # query() is succesful (No error message)
        self.assertNotIn('errors', r.json())

    def test_private_query(self):
        pass

