# Import Built-Ins
import logging
from unittest import TestCase
import time

# Import Third-Party
import requests

# Import Homebrew
from bitex.base import BaseAPI, RESTAPI
from bitex.rest import BitstampREST
from bitex.exceptions import IncompleteCredentialsWarning, IncompleteCredentialsError

# Init Logging Facilities
log = logging.getLogger(__name__)


class BaseAPITests(TestCase):
    def test_base_api_parameters_initialize_correctly(self):
        # Raises an error if a Kwarg wasn't given (i.e. instantiation must
        # specify kwargs explicitly)
        with self.assertRaises(TypeError):
            api = BaseAPI(addr='Bangarang')

        # raise error if address is None
        with self.assertRaises(ValueError):
            api = BaseAPI(addr=None, key=None, secret=None,
                          config=None, version=None)

        # silently initialize if all other parameters are none
        api = BaseAPI(addr='Bangarang', key=None, secret=None, config=None,
                      version=None)

        # if version is None, make version an empty string
        self.assertEqual(api.version, '')

        # if key is None, make key None
        self.assertIs(api.key, None)

        # if secret is None, make secret None
        self.assertIs(api.secret, None)

        # raise warning if only key or only secret is passed
        with self.assertWarns(IncompleteCredentialsWarning):
            api = BaseAPI(addr='Bangarang', key='SomeKey', secret=None,
                          config=None, version=None)
        with self.assertWarns(IncompleteCredentialsWarning):
            api = BaseAPI(addr='Bangarang', key=None, secret='SomeSecret',
                          config=None, version=None)

        # raise a Value Error if an empty string is passed in either key or
        # secret kwarg
        with self.assertRaises(ValueError):
            api = BaseAPI(addr='Bangarang', key='', secret=None,
                          config=None, version=None)
        with self.assertRaises(ValueError):
            api = BaseAPI(addr='Bangarang', key=None, secret='',
                          config=None, version=None)

        # Make sure all attributes are correctly updated if a config file is
        # given
        api = BaseAPI(addr='http://some.api.com', key=None, secret=None,
                      config='/home/nils/git/bitex/tests/config.ini',
                      version=None)
        self.assertEqual(api.addr, 'http://some.api.com')
        self.assertEqual(api.secret, 'panda')
        self.assertEqual(api.key, 'shadow')
        self.assertEqual(api.version, 'v2')

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

        # generate_request_kwargs returns a dict with all necessary keys present
        d = api.sign_request_kwargs('market')
        template = {'method': None, 'url': 'http://some.api.com/v2/market',
                    'headers': None, 'files': None, 'data': None, 'hooks': None,
                    'params': None, 'auth': None, 'cookies': None, 'json': None}
        for k in template:
            self.assertTrue(k in d)

    def test_query_methods_return_as_expected(self):
        # assert that an InvalidCredentialsError is raised, if any of the auth
        # attributes are None (key, secret)
        api = RESTAPI(addr='http://some.api.com', key='shadow', secret=None,
                      version='v2', timeout=5)

        with self.assertRaises(IncompleteCredentialsError):
            api.private_query('GET', 'market', url='https://www.someapi.com')

        api = RESTAPI(addr='http://some.api.com', key=None, secret='panda',
                      version='v2')

        with self.assertRaises(IncompleteCredentialsError):
            api.private_query('GET', 'market', url='https://www.someapi.com')

        api = RESTAPI(addr='http://some.api.com', key=None, secret=None,
                      version='v2')

        with self.assertRaises(IncompleteCredentialsError):
            api.private_query('GET', 'market', url='https://www.someapi.com')

        # assert that _query() silently returns an requests.Response() obj, if
        # the request was good
        resp = api._query('GET', url='http://api.geonames.org/childrenJSON?'
                                     'formatted=true&geonameId=3175395&'
                                     'username=demo&style=full')
        self.assertIsInstance(resp, requests.Response)

        # assert that _query() raises an appropriate error on status code other
        # than 200
        with self.assertRaises(requests.exceptions.HTTPError):
            api._query('data', url='http://api.geonames.org/childrenJSON?'
                                   'formatted=true&geonameId=3175395&'
                                   'username=demo&style=full')
        self.fail("finish this test!")


class BitstampRESTTests(TestCase):
    def test_initialization(self):

        # make sure a warning is displayed upon incomplete credentials
        with self.assertWarns(IncompleteCredentialsWarning):
            api = BitstampREST(addr='Bangarang', user_id=None, key='SomeKey',
                               secret='SomeSecret', config=None, version=None)

        # make sure an exception is raised if user_id is passed as ''
        with self.assertRaises(ValueError):
            api = BitstampREST(addr='Bangarang', user_id='', key='SomeKey',
                               secret='SomeSecret', config=None,
                               version=None)

        # make sure user_id=None is converted to ''
        api = BitstampREST(addr='Bangarang', user_id=None)
        self.assertIs(api.user_id, None)

        # make sure that load_config loads user_id correctly, and issues a
        # warning if user_id param isn't available
        with self.assertWarns(IncompleteCredentialsWarning):
            api = BitstampREST(addr='Bangarang', config='config.ini')

        api = BitstampREST(addr='Bangarang', config='config_bitstamp.ini')
        self.assertEqual(api.user_id, 'testuser')

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        self.fail("Finish this test")

if __name__ == '__main__':
    import unittest
    unittest.main()
