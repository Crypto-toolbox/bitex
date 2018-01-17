"""Base Class TestCase definitions."""
# Import Built-Ins
from unittest import TestCase, mock
import warnings
import logging
import unittest
from unittest.mock import patch
import time

# Import Third-Party
import requests

# Import Homebrew
from bitex.api.base import BaseAPI
from bitex.api.REST import RESTAPI
from bitex.interface.base import Interface
from bitex.interface.rest import RESTInterface

from bitex.exceptions import IncompleteCredentialsWarning
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteAPIConfigurationWarning
from bitex.exceptions import IncompleteCredentialConfigurationWarning


# Init Logging Facilities
log = logging.getLogger(__name__)

try:
    tests_folder_dir = os.environ['TRAVIS_BUILD_DIR'] + '/tests/'
except KeyError:
    tests_folder_dir = '.'


class BaseAPITests(TestCase):
    def test_base_api_parameters_initialize_correctly(self):
        # Raises an error if a Kwarg wasn't given (i.e. instantiation must
        # specify kwargs explicitly)
        with self.assertRaises(TypeError):
            api = BaseAPI(addr='Bangarang')

        # silently initialize if all other parameters are none
        api = BaseAPI(addr='Bangarang', key=None, secret=None, config=None,
                      version=None)

        # if version is None, make version an empty string
        self.assertIs(api.version, None)

        # if key is None, make key None
        self.assertIs(api.key, None)

        # if secret is None, make secret None
        self.assertIs(api.secret, None)

        # raise warning if only key or only secret is passed and config is None
        kwargs = ({'key': 'SomeKey', 'secret': None},
                  {'key': None, 'secret': 'SomeSecret'})
        for auth in kwargs:
            with self.assertWarns(IncompleteCredentialsWarning):
                api = BaseAPI(addr='Bangarang', config=None, version=None,
                              **auth)

        # assert that no warning is raised if credential kwargs are incomplete
        # but a config is passed
        with self.assertRaises(AssertionError,
                               msg='IncompleteCredentialsWarning was raised '
                                   'unexpectedly!'):
            with self.assertWarns(IncompleteCredentialsWarning):
                BaseAPI(addr='Bangarang', key=None, secret='SomeSecret',
                        config="%s/configs/config.ini" % tests_folder_dir,
                        version=None)

        # raise a Value Error if an empty string is passed in either key or
        # secret kwarg
        kwargs = ({'key': '', 'secret': None}, {'key': None, 'secret': ''})
        for auth in kwargs:
            with self.assertRaises(ValueError, msg=auth):
                BaseAPI(addr='Bangarang', config=None, version=None, **auth)

        # Make sure all attributes are correctly updated if a config file is
        # given
        api = BaseAPI(addr='http://some.api.com', key='shadow', secret='panda',
                      config='%s/configs/config.ini' % tests_folder_dir,
                      version='v2')
        self.assertEqual(api.addr, 'http://some.api.com')
        self.assertEqual(api.secret, 'panda')
        self.assertEqual(api.key, 'shadow')
        self.assertEqual(api.version, 'v2')

        # assert that FileNotFoundError is raised if an invalid file path
        # is given
        with self.assertRaises(FileNotFoundError):
            BaseAPI(addr='http://some.api.com', key='shadow', secret='panda',
                    config='%s/configs/file_doesnt_exist.ini' % tests_folder_dir,
                    version=None)

        # Assert that a warning is issued if version is None and 'version'
        # is not present in the passed config file.
        # Assert that a warning is issued if addr is None and 'address'
        # is not present in the passed config file.
        kwargs = ({'version': None, 'addr': 'http://some.api.com'},
                  {'version': 'v2', 'addr': None})
        for api_config in kwargs:
            with self.assertWarns(IncompleteAPIConfigurationWarning,
                                  msg=api_config):
                BaseAPI(key='shadow', secret='panda',
                        config='%s/configs/config_no_api.ini' % tests_folder_dir,
                        **api_config)

        # Make sure nonce() method always supplies increasing Nonce
        previous_nonce = 0
        for i in range(100):
            time.sleep(0.01)
            new_nonce = int(api.nonce())
            self.assertLess(previous_nonce, new_nonce)
            previous_nonce = new_nonce

    @mock.patch('time.time', return_value=1000.1000)
    def test_nonce(self, mock_time):
        self.assertEqual(BaseAPI.nonce(), str(int(round(mock_time() * 1000))))

    def test_load_config(self):
        with self.assertRaises(FileNotFoundError):
            open("non_existant_file.txt")

        no_key_warning_msg = "Key parameter not present in config - authentication may not work!"
        no_secret_warning_msg = "Key parameter not present in config - authentication may not work!"
        no_version_warning_msg = "API version was not present in config - requests may not work!"
        no_url_warning_msg = "API address not present in config - requests may not work!"

        no_key_warning_args = (no_key_warning_msg, IncompleteCredentialConfigurationWarning)
        no_secret_warning_args = (no_secret_warning_msg, IncompleteCredentialConfigurationWarning)
        no_version_warning_args = (no_version_warning_msg, IncompleteAPIConfigurationWarning)
        no_address_warning_args = (no_url_warning_msg, IncompleteAPIConfigurationWarning)

        with mock.patch.object(warnings, 'warn') as mock_warn:
            BaseAPI(config='%s/configs/config_empty.ini' % tests_folder_dir,
                    key=None, secret=None, addr=None, version=None)
            mock_warn.assert_any_call(*no_key_warning_args)
            mock_warn.assert_any_call(*no_secret_warning_args)
            mock_warn.assert_any_call(*no_address_warning_args)
            mock_warn.assert_any_call(*no_version_warning_args)

        with mock.patch.object(warnings, 'warn') as mock_warn:
            BaseAPI(config='%s/configs/config_no_auth.ini' % tests_folder_dir,
                    key=None, secret=None, addr=None, version=None)
            mock_warn.assert_any_call(*no_key_warning_args)
            mock_warn.assert_any_call(*no_secret_warning_args)
            with self.assertRaises(AssertionError):
                mock_warn.assert_any_call(*no_address_warning_args)
            with self.assertRaises(AssertionError):
                mock_warn.assert_any_call(*no_version_warning_args)

        with mock.patch.object(warnings, 'warn') as mock_warn:
            BaseAPI(config='%s/configs/config_no_api.ini' % tests_folder_dir, key=None, secret=None, addr=None,
                    version=None)
            mock_warn.assert_any_call(*no_address_warning_args)
            mock_warn.assert_any_call(*no_version_warning_args)
            with self.assertRaises(AssertionError):
                mock_warn.assert_any_call(*no_key_warning_args)
            with self.assertRaises(AssertionError):
                mock_warn.assert_any_call(*no_secret_warning_args)


class RESTAPITests(TestCase):
    def test_generate_methods_work_correctly(self):
        api = RESTAPI(addr='http://some.api.com', key='shadow', secret='panda',
                      version='v2')

        # generate_uri returns a string of version + endpoint
        uri = api.generate_uri('market')
        self.assertEqual(uri, '/v2/market')

        # generate_url returns a string of address + uri
        self.assertEqual(api.generate_url(uri), 'http://some.api.com/v2/market')

    def test_sign_request_kwargs_method_and_signature(self):
        api = RESTAPI(addr='http://some.api.com', key='shadow', secret='panda',
                      version='v2')
        # generate_request_kwargs returns a dict with all necessary keys present
        d = api.sign_request_kwargs('market')
        template = {'url': 'http://some.api.com/v2/market',
                    'headers': {}, 'files': {}, 'data': {}, 'hooks': {},
                    'params': {}, 'auth': {}, 'cookies': {}, 'json': {}}
        for k in template:
            self.assertTrue(k in d)

    def test_query_methods_return_as_expected(self):
        # assert that an IncompleteCredentialsError is raised, if any of the
        # auth attributes are None (key, secret) when querying a private
        # endpoint of the API.
        kwargs = ({'key': 'shadow', 'secret': None},
                  {'key': None, 'secret': 'panda'},
                  {'key': None, 'secret': None})
        for kw in kwargs:
            api = RESTAPI(addr='http://some.api.com', version='v2', timeout=5,
                          **kw)
            with self.assertRaises(IncompleteCredentialsError, msg=kw):
                api.private_query('GET', 'market', url='https://www.someapi.com')

        # assert that _query() silently returns an requests.Response() obj, if
        # the request was good
        with mock.patch.object(requests, 'request') as mock_request:
            mock_request.return_value = requests.Response()
            resp = RESTAPI('http://test.com')._query('GET', url='https://api.kraken.com/0/public/Time')
            mock_request.assert_called_once_with('GET', timeout=10, url='https://api.kraken.com/0/public/Time')
            self.assertIsInstance(resp, requests.Response)


class InterfaceTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InterfaceTests, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        class ConcreteClass(Interface):
            def __init__(self, *, name, rest_api):
                super(ConcreteClass, self).__init__(name=name, rest_api=rest_api)

            def _get_supported_pairs(self):
                return super(ConcreteClass, self)._get_supported_pairs()

            def is_supported(self, pair):
                return super(ConcreteClass, self).is_supported(pair)

            def request(self, verb, endpoint, authenticate=False, **req_kwargs):
                return super(ConcreteClass, self).request(verb, endpoint, authenticate,
                                                          **req_kwargs)

        cls.interface_cls = ConcreteClass

    def test_supported_pairs_facility(self):
        iface = self.interface_cls(name='TestInterface', rest_api=None)
        self.assertIs(iface.supported_pairs, None)

        # Assert that the supported_pairs attribute cannot be set
        with self.assertRaises(AttributeError):
            iface.supported_pairs = ['Hello']

        # Assert that is_supported() method evaluates as expected. To test this,
        # circumvent overwrite protection of supported_pairs attribute.
        iface._supported_pairs = ['BTCUSD', 'LTCBTC']

        self.assertTrue(iface.is_supported('BTCUSD'))
        self.assertTrue(iface.is_supported('LTCBTC'))
        self.assertFalse(iface.is_supported('LTCUSD'))
        self.assertFalse(iface.is_supported('btcusd'))

        # Assert that, by default, _get_supported_pairs() raises a
        # NotImplementedError
        with self.assertRaises(NotImplementedError):
            iface._get_supported_pairs()

        # Assert that, by default, _supported_pairs is None if _get_supported_pairs is not
        # implemented.
        iface = self.interface_cls(name='CoinCheck', rest_api=None)
        self.assertIsNone(iface._supported_pairs)

    @patch('bitex.api.REST.rest.RESTAPI')
    def test_request_calls_correct_query_method(self, mocked_REST):
        # If ``authenticate=True`` is passed, the Interface should call
        # :meth:``RESTAPI.private_query``, else :meth:``RESTAPI.public_query()`` should be called.
        iface = self.interface_cls(name='TestInterface', rest_api=mocked_REST)
        iface.request('GET', 'th/end/point', authenticate=False)
        self.assertTrue(mocked_REST.public_query.called)
        iface.request('GET', 'th/end/point', authenticate=True)
        self.assertTrue(mocked_REST.private_query.called)


class RESTInterfaceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class ConcreteClass(RESTInterface):
            def __init__(self, name, rest_api):
                super(ConcreteClass, self).__init__(name, rest_api)

            def _get_supported_pairs(self):
                return super(ConcreteClass, self)._get_supported_pairs()

            def is_supported(self, pair):
                return super(ConcreteClass, self).is_supported(pair)

            def request(self, verb, endpoint, authenticate=False, **req_kwargs):
                return super(ConcreteClass, self).request(verb, endpoint, authenticate,
                                                          **req_kwargs)

            def ticker(self, pair, *args, **kwargs):
                super(ConcreteClass, self).ticker(pair, *args, **kwargs)

            def order_book(self, pair, *args, **kwargs):
                super(ConcreteClass, self).order_book(pair, *args, **kwargs)

            def trades(self, pair, *args, **kwargs):
                super(ConcreteClass, self).trades(pair, *args, **kwargs)

            def ask(self, pair, price, size, *args, **kwargs):
                super(ConcreteClass, self).ask(pair, price, size, *args, **kwargs)

            def bid(self, pair, price, size, *args, **kwargs):
                super(ConcreteClass, self).bid(pair, price, size, *args, **kwargs)

            def order_status(self, order_id, *args, **kwargs):
                super(ConcreteClass, self).order_status(order_id, *args, **kwargs)

            def open_orders(self, *order_ids, **kwargs):
                super(ConcreteClass, self).open_orders(*order_ids, **kwargs)

            def cancel_order(self, *order_ids, **kwargs):
                super(ConcreteClass, self).cancel_order(*order_ids, **kwargs)

            def wallet(self, *args, **kwargs):
                super(ConcreteClass, self).wallet(*args, **kwargs)

        cls.interface_cls = ConcreteClass

    def test_abstractmethods_raise_notImplementedError_if_not_properly_overridden(self):
        iface = self.interface_cls('someting fancy', None)
        iface._supported_pairs = ['pair']
        methods = ['ticker', 'order_book', 'trades', 'ask', 'bid', 'order_status', 'open_orders',
                   'cancel_order', 'wallet']
        for method in methods:
            with self.assertRaises(NotImplementedError):
                getattr(iface, method)('pair', 1, 2, 3, 4, 5, 6)  # Add arbitrary number of args

