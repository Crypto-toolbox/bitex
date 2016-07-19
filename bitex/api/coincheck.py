"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging
import hashlib
import hmac
import time
import json

# Import Third-Party
import requests

# Import Homebrew
from bitex.api.api import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class APIError(Exception):
    pass


class API(object):
    """
    Bitstamp cryptocurrency Exchange API.
    Based on Veox' krakenex module.
    """

    def __init__(self, key='', secret=''):
        """Create an object with authentication information.

        :param key: key required to make queries to the API
        :type key: str
        :param secret: private key used to sign API messages
        :type secret: str
        :param conn: connection TODO
        :type conn: krakenex.Connection

        """
        self.key = key
        self.secret = secret
        self.uri = 'https://coincheck.jp'
        self.apiversion = 'api'

    def load_key(self, path):
        """Load key and secret from file.

        Argument:
        :param path: path to keyfile
        :type path: str

        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()

    def _query(self, urlpath, req={}, headers={}):
        """Low-level query handling.

        :param urlpath: API URL path sans host
        :type urlpath: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: connection TODO
        :type conn: krakenex.Connection
        :param headers: HTTPS headers
        :type headers: dict

        """
        url = self.uri + urlpath
        print(url, req, headers)

        if headers:
            r = requests.get(url, req, headers=headers)
        else:
            r = requests.get(url, params=req)

        try:
            response = r.json()
        except:
            print(r.text)
            raise

        if isinstance(response, dict) and 'error' in response:
            print(response)
            raise APIError(response['error'])

        return response

    def query_public(self, method, req={}):
        """API queries that do not require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: connection TODO
        :type conn: krakenex.Connection

        """
        urlpath = '/' + self.apiversion + '/' + method

        return self._query(urlpath, req)

    def query_private(self, method, req={}):
        """API queries that require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: connection TODO
        :type conn: krakenex.Connection

        """
        urlpath ='/' + self.apiversion + '/' + method
        full_path = self.uri + '/' + self.apiversion + '/' + method
        nonce = str(int(1000 * time.time()))

        # sig = nonce + url + req
        data = (nonce + full_path).encode()

        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha256)
        signature = h.hexdigest()
        headers = {"ACCESS-KEY": self.key,
                   "ACCESS-NONCE": nonce,
                   "ACCESS-SIGNATURE": signature}

        return self._query(urlpath, req, headers)


class _API(RESTAPI):
    def __init__(self, passphrase='', key='', secret='', api_version='api',
                 url='https://coincheck.com'):

        super(API, self).__init__(url, api_version=api_version, key=key,
                                  secret=secret)

    def sign(self, *args, **kwargs):

        nonce = str(int(1000 * time.time()))
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        params = json.dumps(params)
        # sig = nonce + url + req
        data = (nonce + kwargs['urlpath'] + params).encode()
        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha256)
        signature = h.hexdigest()
        headers = {"ACCESS-KEY": self.key,
                   "ACCESS-NONCE": nonce,
                   "ACCESS-SIGNATURE": signature}
        url = self.uri + kwargs['urlpath']
        return url, {'headers': headers}
