"""
API Base Classes for BitEx
"""
# Import Built-Ins
import logging
import warnings
import configparser
import time
import os

# Import Third-Party
import requests

# Import Homebrew
from bitex.exceptions import IncompleteCredentialsWarning
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteAPIConfigurationWarning
from bitex.exceptions import IncompleteCredentialConfigurationWarning

# Init Logging Facilities
log = logging.getLogger(__name__)


class BaseAPI:
    """
    BaseAPI provides lowest-common-denominator methods used in all API types.

    It provides a nonce() method, basic configuration loading and Credential
    validity checking method check_auth_requirements(), which should be
    extended in subclasses to cover any additional parameters necessary.
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

        try:
            self.check_auth_requirements()
        except IncompleteCredentialsError:
            if config is None:
                warnings.warn("Incomplete Credentials were given - "
                              "authentication may not work!",
                              IncompleteCredentialsWarning)

        self.addr = addr
        self.key = key if key else None
        self.secret = secret if secret else None
        self.version = version if version else ''
        self.config_file = config
        if self.config_file:
            self.load_config(self.config_file)

    def check_auth_requirements(self):
        """Check that neither self.key nor self.secret are None. If so, this
        method raises an IncompleteCredentialsError. Otherwise returns None.

        Extend this in  child classes if you need to check for further
        required values.

        :raise: IncompleteCredentialsError
        :return: None

        """
        if any(attr is None for attr in (self.key, self.secret)):
            raise IncompleteCredentialsError
        else:
            return

    def load_config(self, fname):
        """
        Load configuration from an ini file. Return it, in case this
        func needs to be extended.
        :param fname: path to file
        :return: configparser.ConfigParser() Obj
        """
        if not os.path.exists(fname):
            raise FileNotFoundError

        conf = configparser.ConfigParser()
        conf.read(fname)
        try:
            self.key = conf['AUTH']['key']
        except KeyError:
            if self.key is None:
                warnings.warn("Key parameter not present in config - "
                              "authentication may not work!",
                              IncompleteCredentialConfigurationWarning)
        try:
            self.secret = conf['AUTH']['secret']
        except KeyError:
            if self.secret is None:
                warnings.warn("Secret parameter not present in config - "
                              "authentication may not work!",
                              IncompleteCredentialConfigurationWarning)
        try:
            self.addr = conf['API']['address']
        except KeyError:
            if self.addr is None:
                warnings.warn("API address not present in config - "
                              "requests may not work!",
                              IncompleteAPIConfigurationWarning)
        try:
            self.version = conf['API']['version']
        except KeyError:
            if self.version == '':
                warnings.warn("API version was not present in config - "
                              "requests may not work!",
                              IncompleteAPIConfigurationWarning)
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
        super(RESTAPI, self).__init__(addr=addr, key=key, secret=secret,
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
        By default, supplies a default URL using generate_uri and generate_url
        :param endpoint: str, API Endpoint
        :param kwargs: Kwargs meant for requests.Request()
        :return: dict, request kwargs
        """
        uri = self.generate_uri(endpoint)
        url = self.generate_url(uri)
        template = {'url': url, 'headers': {}, 'files': {},
                    'data': {}, 'params': {}, 'auth': {}, 'cookies': {},
                    'hooks': {}, 'json': {}}
        template.update(kwargs)
        return template

    def _query(self, method_verb, **request_kwargs):
        """
        Send the request to the API via requests.
        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        resp = requests.request(method_verb, **request_kwargs,
                                timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def private_query(self, method_verb, endpoint, **request_kwargs):
        """Query a private API endpoint requiring signing of the request.

        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param endpoint: str, API Endpoint
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        self.check_auth_requirements()
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
