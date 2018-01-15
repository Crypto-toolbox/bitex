from unittest import TestCase, mock

import requests

from bitex.interface.rest import APIResponse
from bitex import Binance


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code):
        super(MockResponse, self).__init__()
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class StandardizedMethodTests(TestCase):
    def __init__(self, exchange, *args, **kwargs):
        self.exchange = exchange
        super(StandardizedMethodTests, self).__init__(*args, **kwargs)

    @mock.patch('requests.request')
    def _assert_method_passes(self, method_args, method_kwargs, expected_result, mock_json, method, mocked_request_method):
        mocked_request_method.side_effect = [MockResponse({'BTC-USD'}, 200),  # mock supported_pairs
                                 MockResponse(mock_json, 200)]
        resp = method(*method_args, **method_kwargs)
        
        self.assertIsInstance(resp, APIResponse)
        self.assertEqual(method_args, expected_result, resp.formatted)
        return mocked_request_method

    def test_ticker(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['BTC-USD']
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.ticker)

    def test_order_book(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['BTC-USD']
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.order_book)
    
    def test_trades(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['BTC-USD']
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.trades)

    def test_ask(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['BTC-USD', 1000, 50]
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.ask)

    def test_bid(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['BTC-USD', 1000, 50]
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.bid)

    def test_order_status(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['My_Order_ID']
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.order_status)

    def test_open_orders(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = []
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.open_orders)

    def test_cancel_order(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['My_Order_ID']
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.cancel_order)
        
    def test_wallet(self, expected_result, mock_json, method_args=None, method_kwargs=None):
        template_args = ['BTC-USD']
        template_args += method_args or []
        template_kwargs = {}
        method_kwargs.update(method_kwargs or {})
        return self._assert_method_passes(template_args, template_kwargs, expected_result,
                                          mock_json, self.exchange.wallet)


class SMTBinance(StandardizedMethodTests):
    def __init__(self, *args, **kwargs):
        super(SMTBinance, self).__init__(Binance, *args, **kwargs)

    def test_ticker(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_ticker(expected_result, mock_json)

    def test_order_book(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_order_book(expected_result, mock_json)

    def test_trades(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_trades(expected_result, mock_json)

    def test_bid(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_bid(expected_result, mock_json)

    def test_ask(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_ask(expected_result, mock_json)

    def test_open_orders(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_open_orders(expected_result, mock_json)

    def test_order_status(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_order_status(expected_result, mock_json,
                                                  method_args=additional_args)

    def test_cancel_order(self):
        additional_args = ['BTC-USD']
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_cancel_order(expected_result, mock_json,
                                                  method_args=additional_args)

    def test_wallet(self):
        expected_result = tuple()
        mock_json = {}
        super(SMTBinance, self).test_wallet(expected_result, mock_json)