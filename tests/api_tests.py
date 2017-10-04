# Import Built-Ins
import logging
from unittest import TestCase
import time
from json import JSONDecodeError
# Import Third-Party
import requests


# Import Homebrew
from bitex.api.base import BaseAPI
from bitex.api.REST import RESTAPI
from bitex.api.REST import BitstampREST, BitfinexREST, BittrexREST, BTCEREST
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
        try:
            resp = RESTAPI('http://test.com')._query('GET', url='https://api.kraken.com/0/public/Time')
        except requests.exceptions.ConnectionError:
            self.fail("No Internet connection detected to ")
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

        response = api.private_query('POST', 'balance/')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertIn('usd_balance', response.json(), msg=response.json())


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
        config_path = '%s/auth/bitfinex.ini' % tests_folder_dir
        api = BitfinexREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs

        response = api.private_query('POST', 'balances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))


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
        config_path = '%s/auth/bittrex.ini' % tests_folder_dir
        api = BittrexREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'account/getbalances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertTrue(response.json()['success'], msg=response.json())


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
        config_path = '%s/auth/coincheck.ini' % tests_folder_dir
        api = CoincheckREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'accounts/balance')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertTrue(response.json()['success'], msg=response.json())


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
        config_path = '%s/auth/kraken.ini' % tests_folder_dir
        api = KrakenREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('POST', 'private/Balance')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertEqual(response.json()['error'], [], msg=response.json())


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

    @unittest.expectedFailure
    def test_sign_request_kwargs_method_and_signature(self):
        self.fail("Add config ini first!")
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/itbit.ini' % tests_folder_dir
        api = ITbitREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'wallets')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertEqual(response.status_code, 200, msg=response.status_code)
        self.assertNotIn('code', response.json(), msg=response.json())


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
        config_path = '%s/auth/okcoin.ini' % tests_folder_dir
        api = OKCoinREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('POST', 'userinfo.do')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        self.assertTrue(response.json()['result'],
                        msg=(response.json(), api.sign_request_kwargs('userinfo.do')))


class BTCERESTTest(TestCase):
    def test_initialization(self):
        # test that all default values are assigned correctly if No kwargs are
        # given
        api = BTCEREST()
        self.assertIs(api.secret, None)
        self.assertIs(api.key, None)
        self.assertEqual(api.addr, 'https://btc-e.com/api')
        self.assertEqual(api.version, '3')
        self.assertIs(api.config_file, None)

    def test_sign_request_kwargs_method_and_signature(self):
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/btce.ini' % tests_folder_dir
        api = BTCEREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('POST', 'getInfo')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))
        try:
            self.assertEqual(response.json()['success'], 1,
                             msg=(response.json(), api.sign_request_kwargs('getInfo')))
        except JSONDecodeError:
            self.fail("Error during decoding of JSON payload: %s" % response.text)


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
        config_path = '%s/auth/ccex.ini' % tests_folder_dir
        api = CCEXREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('GET', 'getbalances')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))
        try:
            self.assertTrue(response.json()['success'], msg=response.json())
        except JSONDecodeError:
            self.fail("Error during decoding of JSON payload: %s" % response.text)


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
        # Test that the sign_request_kwargs generate appropriate kwargs:
        config_path = '%s/auth/cryptopia.ini' % tests_folder_dir
        api = CryptopiaREST(config=config_path)
        self.assertEqual(api.config_file, config_path)

        # Check signatured request kwargs
        response = api.private_query('POST', 'GetBalance')
        self.assertEqual(response.status_code, 200,
                         msg="Unexpected status code (%s) for request to path "
                             "%s!" % (response.status_code, response.request.url))

        try:
            self.assertTrue(response.json()['Success'], msg=response.json())
        except JSONDecodeError:
            self.fail('test_sign_request_kwargs_method_and_signature(): '
                      'JSONDecodeError for %s' % response._content)


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

        response = api.private_query('GET', 'account/balance')
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
    import unittest
    unittest.main(verbosity=2)
