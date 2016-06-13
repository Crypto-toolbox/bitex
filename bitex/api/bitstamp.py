"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging

# Import Third-Party
import requests
# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)

import json
import urllib.request, urllib.parse, urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64


class APIError(Exception):
    pass

class API(object):
    """
    Bitstamp cryptocurrency Exchange API.
    Based on Veox' krakenex module.

    """

    def __init__(self, key='', secret='', id=''):
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
        self.id = id
        self.uri = 'https://www.bitstamp.net/api'
        self.apiversion = 'v2'

    def load_key(self, path):
        """Load key and secret from file.

        Argument:
        :param path: path to keyfile
        :type path: str

        """
        with open(path, 'r') as f:
            self.id = f.readline().strip()
            self.key = f.readline().strip()
            self.secret = f.readline().strip()

    def _query(self, urlpath, req={}, is_post=False):
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
        print(url, req)

        if is_post:
            r = requests.post(url, data=req)
        else:
            r = requests.get(url, data=req)

        try:
            response = r.json()
        except json.decoder.JSONDecodeError:
            print(r.text)
            raise

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

        return self._query(urlpath, req, is_post=False)

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

        nonce = str(int(time.time() * 1e6))
        #postdata = urllib.parse.urlencode(req)

        # Unicode-objects must be encoded before hashing
        message = nonce + self.id + self.key
        signature = hmac.new(bytes(self.secret, 'utf-8'), bytes(message, 'utf-8'),
                             hashlib.sha256)
        signature = signature.hexdigest().upper()

        req['key'] = self.key
        req['nonce'] = nonce
        req['signature'] = signature



        return self._query(urlpath, req, is_post=True)