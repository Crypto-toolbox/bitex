# Import Built-Ins
import logging
import unittest
from unittest import mock

# Import Third-Party
import requests

# Import Homebrew
try:
    from bitex.interface.rest import APIResponse
except ImportError:
    raise AssertionError("'APIResponse' not implemented!")

# Init Logging Facilities
log = logging.getLogger(__name__)


class APIResponseTests(unittest.TestCase):

    def test_class_instance_handles_like_requestsResponse_instance(self):
        response = mock.MagicMock(spec=requests.Response)
        api_response = APIResponse(response)

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
        self.assertEqual(api_response.response, response)

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

    def test_formatter_methods_raise_NotImplementedError_for_base_class(self):
        response = mock.MagicMock(spec=requests.Response)
        api_response = APIResponse(response)
        with self.assertRaises(NotImplementedError):
            api_response.ticker(None)

        with self.assertRaises(NotImplementedError):
            api_response.order_book(None)

        with self.assertRaises(NotImplementedError):
            api_response.trades(None)

        with self.assertRaises(NotImplementedError):
            api_response.bid(1, 2, 3)

        with self.assertRaises(NotImplementedError):
            api_response.ask(1, 2, 3)

        with self.assertRaises(NotImplementedError):
            api_response.order_status(None)

        with self.assertRaises(NotImplementedError):
            api_response.open_orders(None)

        with self.assertRaises(NotImplementedError):
            api_response.cancel_order(None)

        with self.assertRaises(NotImplementedError):
            api_response.wallet(None)



if __name__ == '__main__':
    unittest.main()
