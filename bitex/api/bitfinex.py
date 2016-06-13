"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging
import json
import hashlib
import hmac
import base64
import time

# Import Third-Party
import requests
# Import Homebrew

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
        self.uri = 'https://api.bitfinex.com'
        self.apiversion = 'v1'

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
        print(url, headers)

        if headers:
            r = requests.post(url, headers=headers)
        else:
            r = requests.get(url, params=req)

        response = r.json()

        if isinstance(response, dict) and 'error' in response:
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
        urlpath = '/' + self.apiversion + '/' + method
        req['request'] = urlpath
        req['nonce'] = str(int(1000 * time.time()))

        js = json.dumps(req)
        data = base64.standard_b64encode(js.encode('utf8'))

        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha384)
        signature = h.hexdigest()
        headers = {"X-BFX-APIKEY": self.key,
                   "X-BFX-SIGNATURE": signature,
                   "X-BFX-PAYLOAD": data}
        print(headers)

        return self._query(urlpath, headers=headers)