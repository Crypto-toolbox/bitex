# Import Built-Ins
import logging
from unittest import TestCase, mock

# Import Third-Party
import requests

# Import Homebrew
from bitex.formatters import APIResponse

# Init Logging Facilities
log = logging.getLogger(__name__)


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code):
        super(MockResponse, self).__init__()
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class BaseInterfaceTests:
    class StandardizedMethodTestCase(TestCase):

        @mock.patch('requests.request')
        def _assert_method_is_called_with_expected_parameters(self, mocked_request_function,
                                                              method_to_test, method_args,
                                                              method_kwargs, expected_request_args,
                                                              expected_request_kwargs):
            method_to_test(*method_args, **method_kwargs)
            mocked_request_function.assert_called_once()
            mocked_request_function.assert_called_with(*expected_request_args,
                                                       **expected_request_kwargs)

        @mock.patch('requests.request')
        def _assert_method_formatter_passes(self, method_args, method_kwargs, expected_result,
                                            mock_json, method, mock_resp):
            """Assert that the given order returns the expected result in the expected format.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param expected_result: The expected Tuple
            :param mock_json: The json data to feed the formatter
            :param method: The method to call
            :param mock_resp: a ``MockedResponse`` instance
            :return: None
            """
            mock_resp.side_effect = [MockResponse({'BTC-USD'}, 200),  # mock supported_pairs
                                     MockResponse(mock_json, 200)]
            resp = method(*method_args, **method_kwargs)

            self.assertIsInstance(resp, APIResponse)
            self.assertEqual(method_args, expected_result, resp.formatted)

        def test_ticker_formatter(self, expected_result, mock_json, method_args=None,
                                  method_kwargs=None):
            template_args = ['BTC-USD']
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.ticker)

        def test_order_book_formatter(self, expected_result, mock_json, method_args=None,
                                      method_kwargs=None):
            template_args = ['BTC-USD']
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.order_book)

        def test_trades_formatter(self, expected_result, mock_json, method_args=None,
                                  method_kwargs=None):
            template_args = ['BTC-USD']
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.trades)

        def test_ask_formatter(self, expected_result, mock_json, method_args=None, method_kwargs=None):
            template_args = ['BTC-USD', 1000, 50]
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.ask)

        def test_bid_formatter(self, expected_result, mock_json, method_args=None, method_kwargs=None):
            template_args = ['BTC-USD', 1000, 50]
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.bid)

        def test_order_status_formatter(self, expected_result, mock_json, method_args=None,
                                        method_kwargs=None):
            template_args = ['My_Order_ID']
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.order_status)

        def test_open_orders_formatter(self, expected_result, mock_json, method_args=None,
                                       method_kwargs=None):
            template_args = []
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.open_orders)

        def test_cancel_order_formatter(self, expected_result, mock_json, method_args=None,
                                        method_kwargs=None):
            template_args = ['My_Order_ID']
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.cancel_order)

        def test_wallet_formatter(self, expected_result, mock_json, method_args=None,
                                  method_kwargs=None):
            template_args = ['BTC-USD']
            template_args += method_args or []
            template_kwargs = {}
            template_kwargs.update(method_kwargs or {})
            self._assert_method_formatter_passes(template_args, template_kwargs, expected_result,
                                                 mock_json, self.exchange.wallet)

