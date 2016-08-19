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
from bitex.http import KrakenHTTP, BitstampHTTP, BitfinexHTTP, GdaxHTTP
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

class OverlayTest(unittest.TestCase):
    """
    Tests that each client returns the expected data
    Serves as BASE Class for all other REST Client tests.
    """
    def setUp(self):
        """
        Adjust this in child classes to load appropriate keys and pairs.
        :return:
        """

        self.pair = ""  # Pair
        self.key = ''  # API Key
        self.secret = ''  # API Secret
        self.exchange = KrakenHTTP(key=self.key, secret=self.secret)  # API Object

    def tearDown(self):
        self.exchange = None
        self.pair = None

    def test_ticker_endpoint(self):
        """
        Calling the ticker endpoint returns a dictionary with the following
        items:
        Current Price, 24h vol, current ask price, current bid price, timestamp.
        Each item contains a string represenation of a float or int.
        """
        r = self.exchange.ticker(self.pair)
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
        """
        Calling the order book endpoint returns a dict with the following
        items:
        asks [price, vol, ts], bids [price, vol, ts]

        If a timestamp for quotes is unavailable, it should be None. If there
        is only a timestamp for the entire order book, use that instead.
        """
        r = self.exchange.order_book(self.pair)
        self.assertIsInstance(r, dict)
        self.assertCountEqual(['asks', 'bids'], list(r.keys()))
        for q in (r['asks'] + r['bids']):
            [self.assertIsInstance(i, str) for i in q]
            try:
                [dec.Decimal(i) for i in q]
            except dec.InvalidOperation:
                self.fail("An element contains non-decimalable items! %s" % q)

    def test_trades_endpoint(self):
        """
        Calling the trades endpoint returns a dict with the following items:
        filled bids [tid, price, amount, time, type], filled asks [tid, price, amount, time, type]

        """
        r = self.exchange.trades(self.pair)

        # returns a dict
        self.assertIsInstance(r, dict)

        # has keys asks, bids
        self.assertCountEqual(['asks', 'bids'], list(r.keys()))

        # All items of each quote are strings; indexes 1-3 are valid strings for
        # the decimal.Decimal() constructor
        for q in (r['asks'] + r['bids']):
            [self.assertIsInstance(i, str) for i in q]

            for item in q[1:4]:
                try:
                    dec.Decimal(item)
                except dec.InvalidOperation:
                    self.fail("An element contains non-decimalable items! %s" % q)

    def test_balance_endpoint(self):
        """
        Calling the balance method returns a dict of currently available funds
        for each tradable asset pair at the exchange, regardless of funding.

        """
        r = self.exchange.balance()
        self.assertIsInstance(r, dict)
        self.assertTrue(r)
        for i in r:
            self.assertIsInstance(r[i], str)
            try:
                dec.Decimal(r[i])
            except dec.InvalidOperation:
                self.fail("A key contains a non-decimalable string! {%s: %s}" % i, r[i])

    def test_orders_endpoint(self):
        """
        Returns a list of all open orders for the user's account.

        orders() method returns a dict of following layout:
        {bids: [[id, price, vol, status, type, time], ..],
         asks: [[id, price, vol, status, type, time], ..]}

        """
        r = self.exchange.orders()
        self.assertIsInstance(r, dict)
        a = ['asks', 'bids']
        b = list(r.keys())
        self.assertCountEqual(a, b)
        for order in [r['asks'] + r['bids']]:
            [self.assertIsInstance(i, str)for i in order]

    def test_add_order_method(self):
        """
        add_order returns a dict of the following layout:
        {tid: '', price: '', amount: '', side: '', type: ''}
        :return:
        """
        r = self.exchange.add_order(0.0001, 10000, self.pair, 'ask', order_type='limit')
        self.assertIsInstance(r, dict)
        a = ['tid','price','amount','side', 'type']
        b = list(r.keys())
        self.assertCountEqual(a, b)
        (self.assertIsInstance(r[i], str)for i in b)

    def test_cancel_order_method(self):
        pass


class KrakenHTTPClientTest(OverlayTest):

    def setUp(self):
        self.pair = "XXBTZUSD"
        self.key_file = '../../keys/kraken.key'
        self.exchange = KrakenHTTP(key_file=self.key_file)


class BitstampHTTPClientTest(OverlayTest):
    def setUp(self):
        self.pair = "btceur"
        self.key_file = '../../keys/bitstamp.key'
        self.exchange = BitstampHTTP(key_file=self.key_file)


class BitfinexHTTPClientTest(OverlayTest):
    def setUp(self):
        self.pair = "btcusd"
        self.key_file = '../../keys/bitfinex.key'
        self.exchange = BitfinexHTTP(key_file=self.key_file)


class GDAXHTTPClientTest(OverlayTest):
    def setUp(self):
        self.pair = "BTC-USD"
        self.key_file = '../../keys/gdax.key'
        self.exchange = GdaxHTTP(key_file=self.key_file)

