# Import Built-Ins
import logging
import json
from unittest import TestCase, mock
from collections import namedtuple


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

    def json(self, **kwargs):
        try:
            return json.loads(self.json_data, **kwargs)
        except TypeError:
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

        def _assert_method_formatter_passes(self, method, method_args, method_kwargs,
                                            mock_resp_json):
            """Assert that the given method returns the expected result in the expected format.

            :param method: The Interface method to call
            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :return: resp
            """
            with mock.patch('requests.request') as mock_request:
                mock_request.side_effect = [MockResponse(mock_resp_json, 200)]
                try:
                    resp = method(*method_args, **method_kwargs)
                except NotImplementedError:
                    raise AssertionError("Interface method %r has not been implemented yet!" % method.__name__)
    
                self.assertIsInstance(resp, APIResponse)
                try:
                    resp.formatted._fields
                except AttributeError:
                    raise AssertionError("APIResponse.formatted does not return "
                                         "namedtuple-like object! Returns %r instead!" % type(resp.formatted))
                except NotImplementedError:
                    raise AssertionError("Formatter method %r has not been implemented yet!" % method.__name__)
                return resp

        def test_ticker_formatter(self, method_args, method_kwargs, mock_resp_json, expected_result):
            """Test the formatter for the ticker endpoint.
            
            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.ticker
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["bid", "ask", "high", "low", "last", "volume", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_order_book_formatter(self, method_args, method_kwargs, mock_resp_json, expected_result):
            """Test the formatter for the order book endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.order_book
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["bids", "asks", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_trades_formatter(self, method_args, method_kwargs, mock_resp_json, expected_result):
            """Test the formatter for the trades endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.trades
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["trades", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_ask_formatter(self, method_args, method_kwargs, mock_resp_json, expected_result):
            """Test the formatter for the ask endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.ask
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["price", "size", "side", "order_id", "order_type", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_bid_formatter(self, method_args, method_kwargs, mock_resp_json, expected_result):
            """Test the formatter for the bid endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.bid
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["price", "size", "side", "order_id", "order_type", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_order_status_formatter(self, method_args, method_kwargs, mock_resp_json,
                                        expected_result):
            """Test the formatter for the order_status endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.order_status
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["price", "size", "side", "order_id", "order_type", "state", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_open_orders_formatter(self, method_args, method_kwargs, mock_resp_json,
                                       expected_result):
            """Test the formatter for the open_orders endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.open_orders
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ['orders', 'timestamp']
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_cancel_order_formatter(self, method_args, method_kwargs, mock_resp_json,
                                        expected_result):
            """Test the formatter for the cancel_order endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.cancel_order
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)
            expected_fields = ["order_id", "successful", "timestamp"]
            for field in expected_fields:
                self.assertIn(field, result.formatted._fields)

        def test_wallet_formatter(self, method_args, method_kwargs, mock_resp_json,
                                  expected_result):
            """Test the formatter for the wallet endpoint.

            :param method_args: Method arguments to pass as ``*args`` to the method.
            :param method_kwargs:  Method keyword arguments to pass as ``**kwargs`` to the method.
            :param mock_resp_json: The json data to return when calling MockResponse class
            :param expected_result: The expected namedtuple to be found in ApiResponse.formatted
            :return: None
            """
            method = self.exchange.wallet
            result = self._assert_method_formatter_passes(method, method_args, method_kwargs, 
                                                          mock_resp_json)

            self.assertIn('timestamp', result.formatted._fields)
            self.fail("Finish this test!")

