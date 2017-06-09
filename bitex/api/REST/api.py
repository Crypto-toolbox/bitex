"""
ABC for Exchange APIs
"""
# Import Built-Ins
import logging
import time
from abc import ABCMeta, abstractmethod

# Import Third-Party
import requests

# Import Homebrew
from bitex.api.REST.response import APIResponse

log = logging.getLogger(__name__)

# Import Built-Ins
import logging
import warnings
import configparser
import time

# Import Third-Party
import requests

# Import Homebrew
from bitex.exceptions import IncompleteCredentialsWarning
# Init Logging Facilities
log = logging.getLogger(__name__)


class BaseAPI:
    """
    BaseAPI provides lowest-common-denominator methods used in all API types.

    It provides a Nonce() method, basic configuration loading and a place-holder
    sign() method.
    """
    def __init__(self, *, addr, key, secret, version, config):
        """
        Initialize a BaseAPI instance.
        :param addr: str, API url
        :param key: str, API key
        :param secret: str, API secret
        :param version: str, version of API to request
        :param config: str, path to config file
        """
        # validate inputs
        if key == '' or secret == '':
            raise ValueError("Invalid key or secret - cannot be empty string! "
                             "Pass None instead!")

        if ((key is None and secret is not None) or
                (key is not None and secret is None)):
            warnings.warn("Incomplete Credentials were given - authentication "
                          "may not work!", IncompleteCredentialsWarning)

        self.addr = addr
        self.key = key if key else None
        self.secret = secret if secret else None
        self.version = version if version else ''
        if config:
            self.load_config(config)

    def load_config(self, fname):
        """
        Load configuration from an ini file. Return it, in case this
        func needs to be extended.
        :param fname: path to file
        :return: configparser.ConfigParser() Obj
        """
        conf = configparser.ConfigParser()
        conf.read(fname)
        self.key = conf['AUTH']['key']
        self.secret = conf['AUTH']['secret']
        self.version = conf['API']['version']
        self.addr = conf['API']['address']
        return conf

    @staticmethod
    def nonce():
        """
        Creates a Nonce value for signature generation
        :return: Nonce as string
        """
        return str(int(1000 * time.time()))


class RESTAPI(BaseAPI):
    """
    Generic REST API interface. Supplies private and public query methods,
    as well as building blocks to customize the signature generation process.
    """
    def __init__(self, addr, timeout=None, key=None, secret=None, version=None,
                 config=None):
        """
        Initializes the RESTAPI instance.
        :param addr: str, API URL (excluding endpoint paths, if applicable)
        :param key: str, API key
        :param secret: str, API secret
        :param config: str, path to config file
        :param timeout: int or float, defines timeout for requests to API
        """
        super(RESTAPI, self).__init__(addr, key=key, secret=secret,
                                      version=version, config=config)
        self.timeout = timeout if timeout else 10

    def generate_uri(self, endpoint):
        """
        Generate a Unique Resource Identifier (API Version + Endpoint)
        :param endpoint: str, endpoint path (i.e. /market/btcusd)
        :return: str, URI
        """
        if self.version:
            return '/' + self.version + '/' + endpoint
        else:
            return '/' + endpoint

    def generate_url(self, uri):
        """
        Generate a Unique Resource Locator (API Address + URI)
        :param uri: str, URI
        :return: str, URL
        """
        return self.addr + uri

    def sign_request_kwargs(self, endpoint, **kwargs):
        """
        Dummy Request Kwarg Signature Generator.
        Extend this to implement signing of requests for private api calls.
        :param endpoint: str, API Endpoint
        :param kwargs: Kwargs meant for requests.Request()
        :return: dict, request kwargs
        """
        uri = self.generate_uri(endpoint)
        url = self.generate_url(uri)
        template = {'method': None, 'url': url, 'headers': None, 'files': None,
                    'data': None, 'params': None, 'auth': None, 'cookies': None,
                    'hooks': None, 'json': None}
        template.update(kwargs)
        return template

    def _query(self, method_verb, **request_kwargs):
        """
        Send the request to the API via requests.
        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        return requests.request(method_verb, **request_kwargs)

    def private_query(self, method_verb, endpoint, **request_kwargs):
        """
        Query a private API endpoint requiring signing of the request.
        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param endpoint: str, API Endpoint
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        request_kwargs = self.sign_request_kwargs(endpoint, **request_kwargs)
        return self._query(method_verb, **request_kwargs)

    def public_query(self, method_verb, endpoint, **request_kwargs):
        """
        Query a public (i.e. unauthenticated) API endpoint and return the result.
        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param endpoint: str, API Endpoint
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        request_kwargs['url'] = self.generate_url(self.generate_uri(endpoint))
        return self._query(method_verb, **request_kwargs)
