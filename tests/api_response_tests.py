# Import Built-Ins
import logging
import unittest
from unittest import mock

# Import Third-Party
import requests

# Import Homebrew
try:
    from bitex.formatters import APIResponse
except ImportError:
    raise AssertionError("'APIResponse' not implemented!")

# Init Logging Facilities
log = logging.getLogger(__name__)


class APIResponseTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(APIResponseTests, self).__init__(*args, **kwargs)
        self.dummy_request = requests.get('https://google.com')

    def test_class_instance_handles_like_requestsResponse_instance(self):
        class TestAPIResponse(APIResponse):
            def ticker(self, bid, ask, high, low, last, volume, ts):
                pass

            def order_book(self, bids, asks, ts):
                pass

            def trades(self, trades, ts):
                pass

            def bid(self, price, size, side, oid, otype, ts):
                pass

            def ask(self, price, size, side, oid, otype, ts):
                pass

        api_response = TestAPIResponse('test_method', self.dummy_request)

        # Assert all expected attributes are present
        expected_attributes = ['apparent_encoding', 'content', 'cookies', 'elapsed', 'encoding',
                               'headers', 'history', 'is_permanent_redirect', 'is_redirect',
                               'links', 'next', 'ok', 'raw', 'reason', 'request', 'status_code',
                               'text', 'url', 'response']
        for attr in expected_attributes:
            self.assertTrue(hasattr(api_response, attr),
                            msg="%s has no attribute '%s'" % (api_response, attr))

        # Assert that we can access the original Response object via the APIResponse.response
        # attribute.
        self.assertEqual(api_response.response, self.dummy_request)

        # Assert that all callable methods of requests.Response are also callable in APIResponse
        try:
            api_response.iter_content()
        except TypeError as e:
            if e.args[0].endswith('object is not callable'):
                self.fail("Method 'iter_content' not implemented!")
            else:
                raise

        try:
            api_response.iter_lines()
        except TypeError as e:
            if e.args[0].endswith('object is not callable'):
                self.fail("Method 'iter_lines' not implemented!")
            else:
                raise

    def test_APIResponse_is_a_meta_class(self):
        response = mock.MagicMock(spec=requests.Response)
        with self.assertRaises(TypeError):
            APIResponse('test_method', response())



if __name__ == '__main__':
    unittest.main(verbosity=2)
