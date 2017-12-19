# Import Built-Ins
import logging
import unittest
from unittest import TestCase, mock
import time
import warnings
import json
from json import JSONDecodeError
import hmac
import hashlib
import base64
import urllib

# Import Third-Party
import requests


# Import Homebrew
from bitex.api.base import BaseAPI
from bitex.api.REST import RESTAPI
from bitex.api.REST import BitstampREST, BitfinexREST, BittrexREST
from bitex.api.REST import HitBTCREST, CCEXREST, CoincheckREST, CryptopiaREST
from bitex.api.REST import ITbitREST, GDAXREST, GeminiREST,  KrakenREST, OKCoinREST
from bitex.api.REST import PoloniexREST, QuoineREST, QuadrigaCXREST, RockTradingREST
from bitex.api.REST import VaultoroREST, YunbiREST, BterREST
from bitex.exceptions import IncompleteCredentialsWarning
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteAPIConfigurationWarning
from bitex.exceptions import IncompleteCredentialConfigurationWarning

# Init Logging Facilities
log = logging.getLogger(__name__)

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
            BaseAPI(config='./configs/config_empty.ini', key=None, secret=None, addr=None,
                    version=None)
            mock_warn.assert_any_call(*no_key_warning_args)
            mock_warn.assert_any_call(*no_secret_warning_args)
            mock_warn.assert_any_call(*no_address_warning_args)
            mock_warn.assert_any_call(*no_version_warning_args)

        with mock.patch.object(warnings, 'warn') as mock_warn:
            BaseAPI(config='./configs/config_no_auth.ini', key=None, secret=None, addr=None,
                    version=None)
            mock_warn.assert_any_call(*no_key_warning_args)
            mock_warn.assert_any_call(*no_secret_warning_args)
            with self.assertRaises(AssertionError):
                mock_warn.assert_any_call(*no_address_warning_args)
            with self.assertRaises(AssertionError):
                mock_warn.assert_any_call(*no_version_warning_args)

        with mock.patch.object(warnings, 'warn') as mock_warn:
            BaseAPI(config='./configs/config_no_api.ini', key=None, secret=None, addr=None,
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


class BitstampRESTTests(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BitstampREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://www.bitstamp.net/api')
        self.assertEqual(api.version, 'v2')
        self.assertIs(api.config_file, None)
        # Assert that a Warning is raised if user_id is None, and BaseAPI's
        # check mechanism is extended properly
        api = BitstampREST(addr='Bangarang', user_id=None, key='SomeKey', secret='SomeSecret',
                           config=None, version=None)
        with mock.patch('warnings.warn') as mock_warn:
            api.load_config('./configs/config.ini')
            mock_warn.assert_called_with("'user_id' not found in config!",
                                         IncompleteCredentialConfigurationWarning)

        # make sure an exception is raised if user_id is passed as ''
        with self.assertRaises(ValueError):
            BitstampREST(addr='Bangarang', user_id='', key='SomeKey', secret='SomeSecret',
                         config=None, version=None)

        # make sure user_id is assigned properly
        api = BitstampREST(addr='Bangarang', user_id='woloho')
        self.assertEqual(api.user_id, 'woloho')

        # Check that a IncompleteCredentialConfigurationWarning is issued if
        # user_id isn't available in config, and no user_id was given.
        with self.assertWarns(IncompleteCredentialConfigurationWarning):
            api = BitstampREST(addr='Bangarang', user_id=None,
                               config='%s/configs/config.ini' %
                               tests_folder_dir)

        # check that user_id is loaded correctly, and no
        # IncompleteCredentialsWarning is issued, if we dont pass a user_id
        # kwarg but it is avaialable in the config file
        config_path = './auth/bitstamp.ini'
        with self.assertRaises(AssertionError):
            with self.assertWarns(IncompleteCredentialConfigurationWarning):
                api = BitstampREST(config=config_path)
        self.assertTrue(api.config_file == config_path)
        self.assertEqual(api.user_id, '267705')

    def test_check_auth_requirements_fires_as_expected_on_empty_user_id(self):
        # config.ini is missing the key 'user_id' and hence should raise
        # an error on checking for authentication credentials when calling check_auth_requirements()
        config_path = '%s/configs/config.ini' % tests_folder_dir
        api = BitstampREST(config=config_path)
        with self.assertRaises(IncompleteCredentialsError):
            api.check_auth_requirements()

    def test_sign_request_kwargs_method_and_signature(self):
        """Test signature generation.


        Example as seen on https://www.bitstamp.net/api/
        ```
        import hmac
        import hashlib

        message = nonce + customer_id + api_key
        signature = hmac.new(API_SECRET, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        ```
        """
        # Test that the sign_request_kwargs generate appropriate kwargs:

        # Check signatured request kwargs
        key, secret, user = 'panda', 'shadow', 'leeroy'
        with mock.patch.object(RESTAPI, 'nonce', return_value=str(10000)) as mock_rest:
            api = BitstampREST(key=key, secret=secret, user_id=user)
            ret_values = api.sign_request_kwargs('testing/signature', param_1='a', param_2=1)
            expected_signature = hmac.new(secret.encode('utf-8'),
                                          (str(10000) + user + key).encode('utf-8'),
                                          hashlib.sha256).hexdigest().upper()
            self.assertIn('key', ret_values['data'])
            self.assertEqual(ret_values['data']['key'], key)
            self.assertIn('signature', ret_values['data'])
            self.assertEqual(ret_values['data']['signature'], expected_signature)
            self.assertIn('nonce', ret_values['data'])
            self.assertEqual(ret_values['data']['nonce'], str(10000))


class BitfinexRESTTests(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BitfinexREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.bitfinex.com')
        self.assertEqual(api.version, 'v1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret = 'panda', 'shadow'
        with mock.patch.object(RESTAPI, 'nonce', return_value=str(100)):
            api = BitfinexREST(key=key, secret=secret)
            self.assertEqual(api.nonce(), str(100))
            self.assertEqual(api.version, 'v1')
            self.assertEqual(api.generate_uri('testing/signature'), '/v1/testing/signature')
            ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'})
            possible_json_dumps = ['{"param_1": "abc", "nonce": "100", "request": "/v1/testing/signature"}',
                                   '{"param_1": "abc", "request": "/v1/testing/signature", "nonce": "100"}',
                                   '{"nonce": "100", "param_1": "abc", "request": "/v1/testing/signature"}',
                                   '{"nonce": "100", "request": "/v1/testing/signature", "param_1": "abc"}',
                                   '{"request": "/v1/testing/signature", "param_1": "abc", "nonce": "100"}',
                                   '{"request": "/v1/testing/signature", "nonce": "100", "param_1": "abc"}']
            data = [base64.standard_b64encode(pl.encode('utf8'))
                    for pl in possible_json_dumps]
            signatures = [hmac.new(secret.encode('utf-8'), d, hashlib.sha384).hexdigest()
                          for d in data]

            self.assertIn('X-BFX-APIKEY', ret_values['headers'])
            self.assertEqual(ret_values['headers']['X-BFX-APIKEY'], key)
            self.assertIn('X-BFX-PAYLOAD', ret_values['headers'])
            self.assertIn(ret_values['headers']['X-BFX-PAYLOAD'], data)
            self.assertIn('X-BFX-SIGNATURE', ret_values['headers'])
            self.assertIn(ret_values['headers']['X-BFX-SIGNATURE'], signatures)


class BittrexRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BittrexREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://bittrex.com/api')
        self.assertEqual(api.version, 'v1.1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret, user = 'panda', 'shadow', 'leeroy'
        with mock.patch.object(RESTAPI, 'nonce', return_value=str(100)) as mock_rest:
            api = BittrexREST(key=key, secret=secret, version='v1.1')
            self.assertEqual(api.generate_uri('testing/signature'), '/v1.1/testing/signature')
            ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'})
            url = 'https://bittrex.com/api/v1.1/testing/signature?apikey=panda&nonce=100&param_1=abc'
            sig = hmac.new(secret.encode('utf8'), url.encode('utf8'), hashlib.sha512).hexdigest()
            self.assertEqual(ret_values['url'], url)
            self.assertIn('apisign', ret_values['headers'])
            self.assertEqual(ret_values['headers']['apisign'], sig)


class CoinCheckRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = CoincheckREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://coincheck.com')
        self.assertEqual(api.version, 'api')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret, user = 'panda', 'shadow', 'leeroy'
        with mock.patch.object(RESTAPI, 'nonce', return_value=str(100)) as mock_rest:
            api = CoincheckREST(key=key, secret=secret, version='v1')
            self.assertEqual(api.generate_uri('testing/signature'), '/v1/testing/signature')
            ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'})
            msg = '100https://coincheck.com/v1/testing/signature?param_1=abc'
            sig = hmac.new(secret.encode('utf8'), msg.encode('utf8'), hashlib.sha256).hexdigest()
            self.assertIn('ACCESS-NONCE', ret_values['headers'])
            self.assertEqual(ret_values['headers']['ACCESS-NONCE'], "100")
            self.assertIn('ACCESS-KEY', ret_values['headers'])
            self.assertEqual(ret_values['headers']['ACCESS-KEY'], key)
            self.assertIn('ACCESS-SIGNATURE', ret_values['headers'])
            self.assertEqual(ret_values['headers']['ACCESS-SIGNATURE'], sig)


class GDAXRESTTest(TestCase):
    @unittest.expectedFailure
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = GDAXREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertIs(api.passphrase, None)
        self.assertEqual(api.addr, 'https://api.gdax.com')
        self.assertIs(api.version, None)
        self.assertIs(api.config_file, None)
        # Assert that a Warning is raised if passphrase is None, and BaseAPI's
        # check mechanism is extended properly
        with self.assertWarns(IncompleteCredentialsWarning):
            api = GDAXREST(addr='Bangarang', passphrase=None, key='SomeKey',
                           secret='SomeSecret', config=None, version=None)

        # make sure an exception is raised if passphrase is passed as ''
        with self.assertRaises(ValueError):
            api = GDAXREST(addr='Bangarang', passphrase='', key='SomeKey',
                           secret='SomeSecret', config=None, version=None)

        # make sure user_id is assigned properly
        api = GDAXREST(addr='Bangarang', passphrase='woloho')
        self.assertIs(api.passphrase, 'woloho')

        # Check that a IncompleteCredentialConfigurationWarning is issued if
        # user_id isn't available in config, and no user_id was given.
        with self.assertWarns(IncompleteCredentialConfigurationWarning):
            api = GDAXREST(addr='Bangarang', passphrase=None,
                           config='%s/configs/config.ini' % tests_folder_dir)

        # check that passphrase is loaded correctly, and no
        # IncompleteCredentialsWarning is issued, if we dont pass a passphrase
        # kwarg but it is avaialable in the config file
        self.fail("Add config ini first!")
        config_path = '/home/nls/git/bitex/tests/auth/gdax.ini'
        with self.assertRaises(AssertionError):
            with self.assertWarns(IncompleteCredentialConfigurationWarning):
                api = GDAXREST(config=config_path)
        self.assertTrue(api.config_file == config_path)
        self.assertEqual(api.passphrase, 'testuser')

    @unittest.expectedFailure
    def test_sign_request_kwargs_method_and_signature(self):
        self.fail("Add config ini first!")
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/gdax.ini' % tests_folder_dir
        api = GDAXREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'accounts')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertEqual(response.status_code, 200, msg=response.status_code)
        self.assertIn('id', response.json()[0], msg=response.json())


class KrakenRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = KrakenREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.kraken.com')
        self.assertEqual(api.version, '0')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key = 'panda'
        secret = '11LX0lqM9aExe63oe975Fjms5I9plFAPDxj0puwFBKGct79CP9GESjl5IRTDP8bqNaMYWXxEO8UbM0e4kacRtw=='
        with mock.patch.object(RESTAPI, 'nonce', return_value=str(100)) as mock_rest:
            api = KrakenREST(key=key, secret=secret, version='api')
            self.assertEqual(api.generate_uri('testing/signature'), '/api/testing/signature')
            ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'})
            encoded_payloads = ('nonce=100&param_1=abc', 'param_1=abc&nonce=100')
            expected_payload = {'nonce': '100', 'param_1': 'abc'}
            sigs = []
            for pl in encoded_payloads:
                encoded = ('100' + pl).encode()
                msg = '/api/testing/signature'.encode('utf-8') + hashlib.sha256(encoded).digest()
                signature = hmac.new(base64.b64decode(secret), msg, hashlib.sha512)
                sigdigest = base64.b64encode(signature.digest())
                sigs.append(sigdigest.decode('utf-8'))
            self.assertIn('API-Key', ret_values['headers'])
            self.assertEqual(ret_values['headers']['API-Key'], key)
            self.assertIn('API-Sign', ret_values['headers'])
            self.assertIn(ret_values['headers']['API-Sign'], sigs)
            self.assertEqual(ret_values['data'], expected_payload)


class ITBitRESTTest(TestCase):
    @unittest.expectedFailure
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = ITbitREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.itbit.com')
        self.assertEqual(api.version, 'v1')
        self.assertIs(api.config_file, None)
        # Assert that a Warning is raised if user_id is None, and BaseAPI's
        # check mechanism is extended properly
        with self.assertWarns(IncompleteCredentialsWarning):
            api = ITbitREST(addr='Bangarang', user_id=None, key='SomeKey',
                            secret='SomeSecret', config=None, version=None)

        # make sure an exception is raised if user_id is passed as ''
        with self.assertRaises(ValueError):
            api = ITbitREST(addr='Bangarang', user_id='', key='SomeKey',
                            secret='SomeSecret', config=None, version=None)

        # make sure user_id is assigned properly
        api = ITbitREST(addr='Bangarang', user_id='woloho')
        self.assertIs(api.user_id, 'woloho')

        # Check that a IncompleteCredentialConfigurationWarning is issued if
        # user_id isn't available in config, and no user_id was given.
        with self.assertWarns(IncompleteCredentialConfigurationWarning):
            api = ITbitREST(addr='Bangarang', user_id=None,
                            config='%s/configs/config.ini' % tests_folder_dir)

        # check that passphrase is loaded correctly, and no
        # IncompleteCredentialsWarning is issued, if we dont pass a user_id
        # kwarg but it is avaialable in the config file
        self.fail("Add config ini first!")
        config_path = '/home/nls/git/bitex/tests/auth/itbit.ini'
        with self.assertRaises(AssertionError):
            with self.assertWarns(IncompleteCredentialConfigurationWarning):
                api = ITbitREST(config=config_path)
        self.assertTrue(api.config_file == config_path)
        self.assertEqual(api.user_id, 'testuser')

    def test_sign_request_kwargs_method_and_signature(self):
        """Test itBit signature methoc.

        ItBit requires both a Nonce value AND a timestamp value. Assert that both methods work
        correctly:
            nnoce() : returns an ever increasing int, starting at 1
            timestamp() : returns a unix timestamp in milliseconds
        """
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret, user = 'panda', 'shadow', 'leeroy'
        with mock.patch.object(ITbitREST, 'timestamp', return_value=str(1000)) as mock_rest:
            api = ITbitREST(key=key, secret=secret, version='v1', user_id=user)
            self.assertEqual(api.generate_uri('testing/signature'), '/v1/testing/signature')
            
            """
            Assert PUT/POST requests are signed correctly. These are the only edge cases as their
            body (i.e. parameters) need to be passed in the header's 'Authorization' parameter,
            instead of passing it to requests.request()'s ``data`` parameter.
            """
            req_url = 'https://api.itbit.com/v1/testing/signature'
            json_bodies = ['{"param_1": "abc"}']
            req_strings = [['POST', 'https://api.itbit.com/v1/testing/signature',
                           '{"param_1": "abc"}', '1', '1000'],
                           ['PUT', 'https://api.itbit.com/v1/testing/signature',
                            '{"param_1": "abc"}', '2', '1000'],
                           ['GET', 'https://api.itbit.com/v1/testing/signature', '', '3', '1000']]
            signatures = []
            for i, req_string in enumerate(req_strings):
                message = json.dumps(req_string, separators=(',', ':'))
                nonced = str(i+1) + message
                hasher = hashlib.sha256()
                hasher.update(nonced.encode('utf-8'))
                hash_digest = hasher.digest()
                hmac_digest = hmac.new(secret.encode('utf-8'),
                                       req_url.encode('utf-8') + hash_digest,
                                       hashlib.sha512).digest()
                signatures.append(user + ':' + base64.b64encode(hmac_digest).decode('utf-8'))
            post_ret_values = api.sign_request_kwargs('testing/signature', 
                                                      params={'param_1': 'abc'}, method='POST')
            put_ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'},
                                                     method='PUT')
            
            self.assertIn('Authorization', post_ret_values['headers'])
            self.assertIn(post_ret_values['headers']['Authorization'], signatures[0])
            self.assertIn('X-Auth-Timestamp', post_ret_values['headers'])
            self.assertEqual(post_ret_values['headers']['X-Auth-Timestamp'], '1000')
            self.assertIn('X-Auth-Nonce', post_ret_values['headers'])
            self.assertEqual(post_ret_values['headers']['X-Auth-Nonce'], '1')
            self.assertIn('Content-Type', post_ret_values['headers'])
            self.assertEqual(post_ret_values['headers']['Content-Type'], 'application/json')
            self.assertIn(post_ret_values['data'], json_bodies)

            self.assertIn('Authorization', put_ret_values['headers'])
            self.assertIn(put_ret_values['headers']['Authorization'], signatures[1])
            self.assertIn('X-Auth-Timestamp', put_ret_values['headers'])
            self.assertEqual(put_ret_values['headers']['X-Auth-Timestamp'], '1000')
            self.assertIn('X-Auth-Nonce', put_ret_values['headers'])
            self.assertEqual(put_ret_values['headers']['X-Auth-Nonce'], '2')
            self.assertIn('Content-Type', put_ret_values['headers'])
            self.assertEqual(put_ret_values['headers']['Content-Type'], 'application/json')
            self.assertIn(put_ret_values['data'], json_bodies)

            """
            Assert Non-PUT/POST requests are signed correctly. Since DELETE and GET methods for itBit
            have the parameters present right in the endpoint, json_body needs to be an emptry 
            string.
            """

            get_ret_values = api.sign_request_kwargs('testing/signature', 
                                                      params={}, method='GET')
            self.assertIn('Authorization', get_ret_values['headers'])
            self.assertEqual(get_ret_values['headers']['Authorization'], signatures[2])
            self.assertIn('X-Auth-Timestamp', get_ret_values['headers'])
            self.assertEqual(get_ret_values['headers']['X-Auth-Timestamp'], '1000')
            self.assertIn('X-Auth-Nonce', get_ret_values['headers'])
            self.assertEqual(get_ret_values['headers']['X-Auth-Nonce'], '3')
            self.assertIn('Content-Type', get_ret_values['headers'])
            self.assertEqual(get_ret_values['headers']['Content-Type'], 'application/json')
            self.assertEqual(get_ret_values['data'], '')


class OKCoinRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = OKCoinREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://www.okcoin.com/api')
        self.assertEqual(api.version, 'v1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret = 'panda', 'shadow'

        api = OKCoinREST(key=key, secret=secret, version='v1')
        self.assertEqual(api.generate_uri('testing/signature'), '/v1/testing/signature')
        ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'},
                                                                          method='POST')
        expected_params = {'api_key': key, 'param_1': 'abc'}
        sign = '&'.join([k + '=' + expected_params[k] for k in sorted(expected_params.keys())])
        sign += '&secret_key=' + secret
        signature = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()
        url = 'https://www.okcoin.com/api/v1/testing/signature'
        self.assertEqual(ret_values['url'], url)
        self.assertIn('api_key=' + key, ret_values['data'])
        self.assertIn('param_1=abc', ret_values['data'])
        self.assertIn('sign=' + signature, ret_values['data'])
        self.assertIn('Content-Type', ret_values['headers'])
        self.assertIn(ret_values['headers']['Content-Type'], 'application/x-www-form-urlencoded')

        url = 'https://www.okcoin.com/api/v1/testing/signature'
        ret_values = api.sign_request_kwargs('testing/signature', params={'param_1': 'abc'},
                                             method='GET')
        self.assertEqual(ret_values['url'], url)
        self.assertEqual(ret_values['data']['api_key'], key)
        self.assertEqual(ret_values['data']['sign'], signature)
        self.assertIn('param_1', ret_values['data'])
        self.assertEqual(ret_values['data']['param_1'], 'abc')

class CCEXRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = CCEXREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://c-cex.com/t')
        self.assertIs(api.version, None)
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret = 'panda', 'shadow'
        with mock.patch.object(RESTAPI, 'nonce', return_value='100'):
            api = CCEXREST(key=key, secret=secret, version='v1')
            ret_values = api.sign_request_kwargs('test_signature', params={'param_1': 'abc'},
                                                 method='GET')
            expected_params = {'api_key': key, 'param_1': 'abc', 'nonce': '100',
                               'a': 'test_signature'}
            sign = '&'.join([k + '=' + expected_params[k] for k in sorted(expected_params.keys())])
            sign += '&secret_key=' + secret
            url = 'https://c-cex.com/t/api.html?a=test_signature&apikey=%s&nonce=100&param_1=abc' % key
            signature = hmac.new(secret.encode('utf-8'), url.encode('utf-8'), hashlib.sha512).hexdigest()
            self.assertEqual(ret_values['url'], url)
            self.assertIn('apisign', ret_values['headers'])
            self.assertEqual(ret_values['headers']['apisign'], signature)


class CryptopiaRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = CryptopiaREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://www.cryptopia.co.nz/api')
        self.assertIs(api.version, None)
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        """Test Cryptopia signature method.

        Reference:
            https://github.com/Coac/cryptopia.js/blob/3b653c4530e730d1d14052cf2c606de88aec0962/index.js#L56
        """
        # Test that the sign_request_kwargs generate appropriate kwargs:
        key, secret = 'panda', 'shadow'
        with mock.patch.object(RESTAPI, 'nonce', return_value='100'):
            api = CryptopiaREST(key=key, secret=secret, version='v1')
            ret_values = api.sign_request_kwargs('test_signature', params={'param_1': 'abc'})
            url = 'https://www.cryptopia.co.nz/api/v1/test_signature'
            expected_params = {'param_1': 'abc'}
            post_data = json.dumps(expected_params)
            md5 = hashlib.md5()
            md5.update(post_data.encode('utf-8'))
            rcb64 = base64.b64encode(md5.digest())
            sig = (key + 'POST' + urllib.parse.quote_plus(url).lower() + '100' +
                   rcb64.decode('utf8'))
            hmac_sig = base64.b64encode(hmac.new(base64.b64encode(secret.encode('utf-8')),
                                                 sig.encode('utf-8'),
                                                 hashlib.sha256).digest())
            signature = 'amx ' + key + ':' + hmac_sig.decode('utf-8') + ':' + '100'
            self.assertEqual(ret_values['data'], json.dumps(expected_params))
            self.assertIn('Authorization', ret_values['headers'])
            self.assertEqual(ret_values['headers']['Authorization'], signature)


class GeminiRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = GeminiREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.gemini.com')
        self.assertEqual(api.version, 'v1')
        self.assertIs(api.config_file, None)

    @unittest.expectedFailure
    def test_sign_request_kwargs_method_and_signature(self):
        self.fail("Add config ini first!")
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/gemini.ini' % tests_folder_dir
        api = GeminiREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'balances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertIn('currency', response.json(), msg=response.json())


class YunbiRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = YunbiREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://yunbi.com/api')
        self.assertIs(api.version, 'v2')
        self.assertIs(api.config_file, None)

    @unittest.expectedFailure
    def test_sign_request_kwargs_method_and_signature(self):
        self.fail("Add config ini first!")
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/yunbi.ini' % tests_folder_dir
        api = YunbiREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'deposits.json')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertNotIn('error', response.json(), msg=response.json())


class RockTradingRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = RockTradingREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.therocktrading.com')
        self.assertEqual(api.version, 'v1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/rocktrading.ini' % tests_folder_dir
        api = RockTradingREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'balances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertIn('balances', response.json(), msg=response.json())


class PoloniexRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = PoloniexREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://poloniex.com')
        self.assertIs(api.version, None)
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/poloniex.ini' % tests_folder_dir
        api = PoloniexREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('POST', 'returnBalances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertNotIn('error', response.json(), msg=(response.json(), response.request.url))


class QuoineRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = QuoineREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.quoine.com/')
        self.assertIs(api.version, '2')
        self.assertIs(api.config_file, None)

    @unittest.expectedFailure
    def test_sign_request_kwargs_method_and_signature(self):
        self.fail("Add config ini first!")
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/quoine.ini' % tests_folder_dir
        api = QuoineREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'fiat_accounts')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertIn('currency', response.json()[0], msg=response.json())


class QuadrigaCXRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = QuadrigaCXREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.quadrigacx.com')
        self.assertEqual(api.version, 'v2')
        self.assertIs(api.config_file, None)
        # Assert that a Warning is raised if client_id is None, and BaseAPI's
        # check mechanism is extended properly
        with self.assertWarns(IncompleteCredentialsWarning):
            api = QuadrigaCXREST(addr='Bangarang', client_id=None, key='SomeKey',
                            secret='SomeSecret', config=None, version=None)

        # make sure an exception is raised if client_id is passed as ''
        with self.assertRaises(ValueError):
            api = QuadrigaCXREST(addr='Bangarang', client_id='', key='SomeKey',
                            secret='SomeSecret', config=None, version=None)

        # make sure client_id is assigned properly
        api = QuadrigaCXREST(addr='Bangarang', client_id='woloho')
        self.assertIs(api.client_id, 'woloho')

        # Check that a IncompleteCredentialConfigurationWarning is issued if
        # client_id isn't available in config, and no client_id was given.
        with self.assertWarns(IncompleteCredentialConfigurationWarning):
            api = QuadrigaCXREST(addr='Bangarang', client_id=None,
                            config='%s/configs/config.ini' % tests_folder_dir)

        # check that passphrase is loaded correctly, and no
        # IncompleteCredentialsWarning is issued, if we dont pass a client_id
        # kwarg but it is avaialable in the config file
        config_path = '%s/auth/quadrigacx.ini' % tests_folder_dir
        with self.assertRaises(AssertionError):
            with self.assertWarns(IncompleteCredentialConfigurationWarning):
                api = QuadrigaCXREST(config=config_path)
        self.assertTrue(api.config_file == config_path)
        self.assertEqual(api.client_id, '2110184')

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/quadrigacx.ini' % tests_folder_dir
        api = QuadrigaCXREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('POST', 'balance')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertIn('cad_balance', response.json(), msg=response.json())


class HitBTCRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = HitBTCREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'http://api.hitbtc.com/api')
        self.assertEqual(api.version, '1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/hitbtc.ini' % tests_folder_dir
        api = HitBTCREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs

        response = api.private_query('GET', 'trading/balance')
        if response.status_code == 401:
            try:
                self.fail('Authorization failed: %s' % response.json())
            except JSONDecodeError:
                pass
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertIn('balance', response.text, msg=response.request.url)


class VaultoroRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = VaultoroREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.vaultoro.com')
        self.assertIs(api.version, None)
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/vaultoro.ini' % tests_folder_dir
        api = VaultoroREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', '1/balance')
        if response.status_code > 499:
            log.error("Server unreachable!")
            return
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertEqual(response.json()['status'], 'success',
                         msg=response.json())


class BterRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BterREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'http://data.bter.com/api2')
        self.assertIs(api.version, '1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/bter.ini' % tests_folder_dir
        api = BterREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Assert signatured request kwargs are valid and api call is succesful
        response = api.private_query('POST', 'private/balances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertTrue(response.json()['result'], msg=response.json())


if __name__ == '__main__':
    unittest.main(verbosity=2)
