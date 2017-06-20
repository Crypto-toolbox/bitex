# Import Built-Ins
import logging
from unittest import TestCase
import time

# Import Third-Party
import requests

# Import Homebrew
from bitex.base import BaseAPI, RESTAPI
from bitex.rest import BitstampREST, BitfinexREST, BittrexREST
from bitex.exceptions import IncompleteCredentialsWarning
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteAPIConfigurationWarning
from bitex.exceptions import IncompleteCredentialConfigurationWarning

# Init Logging Facilities
log = logging.getLogger(__name__)

tests_folder_dir = '/home/nls/git/bitex/tests'


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
        self.assertEqual(api.version, '')

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
        # assert that an IncompleteCredentialsError is raised, if any of the auth
        # attributes are None (key, secret) when querying a private endpoint
        # of the API.
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
        try:
            resp = RESTAPI('http://test.com')._query('GET',
                                                     url='https://api.kraken.com/0/public/Time')
        except requests.exceptions.ConnectionError:
            self.fail("No Internet connection detected to ")
        self.assertIsInstance(resp, requests.Response)

        # assert that _query() raises an appropriate error on status code other
        # than 200
        with self.assertRaises(requests.exceptions.HTTPError):
            RESTAPI('http://test.com')._query('data',
                                              url='https://api.kraken.com/0/public/Wasabi')
        self.fail("finish this test!")


class BitstampRESTTests(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BitstampREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://www.bitstamp.net/api')
        self.assertIs(api.version, '')
        self.assertIs(api.config_file, None)
        # Assert that a Warning is raised if user_id is None, and BaseAPI's
        # check mechanism is extended properly
        with self.assertWarns(IncompleteCredentialsWarning):
            api = BitstampREST(addr='Bangarang', user_id=None, key='SomeKey',
                               secret='SomeSecret', config=None, version=None)

        # make sure an exception is raised if user_id is passed as ''
        with self.assertRaises(ValueError):
            api = BitstampREST(addr='Bangarang', user_id='', key='SomeKey',
                               secret='SomeSecret', config=None,
                               version=None)

        # make sure user_id is assigned properly
        api = BitstampREST(addr='Bangarang', user_id='woloho')
        self.assertIs(api.user_id, 'woloho')

        # Check that a IncompleteCredentialConfigurationWarning is issued if
        # user_id isn't available in config, and no user_id was given.
        with self.assertWarns(IncompleteCredentialConfigurationWarning):
            api = BitstampREST(addr='Bangarang', user_id=None,
                               config='/home/nls/git/bitex/tests/configs/config.ini')

        # check that user_id is loaded correctly, and no
        # IncompleteCredentialsWarning is issued, if we dont pass a user_id
        # kwarg but it is avaialable in the config file
        config_path = '/home/nls/git/bitex/tests/auth/bitstamp.ini'
        with self.assertRaises(AssertionError):
            with self.assertWarns(IncompleteCredentialConfigurationWarning):
                api = BitstampREST(config=config_path)
        self.assertTrue(api.config_file == config_path)
        self.assertEqual(api.user_id, 'testuser')

    def test_private_query_raises_error_on_incomplete_credentials(self):
        # config.ini is missing the key 'user_id' and hence should raise
        # an error on attempting to query a private endpoint.
        config_path = '%s/configs/config.ini' % tests_folder_dir
        api = BitstampREST(config=config_path)
        with self.assertRaises(IncompleteCredentialsError):
            api.private_query('POST', 'balance')

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/bitstamp.ini' % tests_folder_dir
        api = BitstampREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        self.fail("Finish this test")


class BitfinexRESTTests(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BitfinexREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://api.bitfinex.com')
        self.assertIs(api.version, 'v1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/bitfinex.ini' % tests_folder_dir
        api = BitfinexREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        self.fail("Finish this test")


class BittrexRESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BittrexREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://bittrex.com/api')
        self.assertIs(api.version, 'v1.1')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/bittrex.ini' % tests_folder_dir
        api = BittrexREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        self.fail("Finish this test")


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
