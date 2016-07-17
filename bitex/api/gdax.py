"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import time
import hashlib
import hmac
import base64

# Import Third-Party
import requests
from requests.auth import AuthBase

# Import Homebrew
from bitex.api.api import RESTAPI


class APIError(Exception):
    pass


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key.encode()
        self.secret_key = secret_key.encode()
        self.passphrase = passphrase.encode()

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class API(RESTAPI):
    def __init__(self, passphrase='', key='', secret='', api_version='',
                 url='https://api.gdax.com'):
        self.passphrase = passphrase
        super(API, self).__init__(url, api_version=api_version, key=key,
                                  secret=secret)

    def load_key(self, path):
        """
        Load key and secret from file.
        """
        with open(path, 'r') as f:
            self.passphrase = f.readline().strip()
            self.key = f.readline().strip()
            self.secret = f.readline().strip()

    def sign(self, endpoint, *args, **kwargs):
        auth = CoinbaseExchangeAuth(self.key, self.secret,
                                              self.passphrase)
        try:
            js = kwargs['json']
        except KeyError:
            js = {}

        return {'json': js, 'auth': auth}
