"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging
import unittest
import requests
import decimal as dec
# Import Third-Party

# Import Homebrew
from bitex.api.api import RESTAPI
from bitex.http import KrakenHTTP
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


class OverlayTest(unittest.TestCase):
    """
    Tests that each client returns the expected data
    """
    def setUp(self):
        self.exchange = KrakenHTTP()

    def tearDown(self):
        self.exchange = None

    def test_ticker_endpoint(self):
        """
        Calling the ticker endpoint returns a dictionary with the following
        items:
        Current Price, 24h vol, current ask price, current bid price, timestamp.
        Each item contains a string represenation of a float or int.
        :return:
        """
        r = self.exchange.ticker('XXBTZUSD')
        self.assertIsInstance(r, dict)
        a = ['last', '24h Vol', 'ask', 'bid', 'timestamp']
        b = list(r.keys())
        self.assertCountEqual(a, b)
        for key in r:
            self.assertIsInstance(r[key], str)
            try:
                dec.Decimal(r[key])
            except ValueError:
                self.fail("%s could not be converted to Decimal!" % r[key])

    def test_orderbook_endpoint(self):
        pass

    def test_trades_endpoint(self):
        pass

    def test_balance_endpoint(self):
        pass

    def test_orders_endpoint(self):
        pass

    def test_ledger_endpoint(self):
        pass

    def test_add_order_method(self):
        pass

    def test_cancel_order_method(self):
        pass

    def test_fees_method(self):
        pass