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
from bitex.api.api import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class APIError(Exception):
    pass


class API(RESTAPI):
    def __init__(self, key='', secret='', api_version='v1',
                 url='https://api.bitfinex.com'):
        super(API, self).__init__(url, api_version=api_version,
                                  key=key, secret=secret)

    def sign(self, *args, **kwargs):
        try:
            req = kwargs['params']
        except KeyError:
            req = {}
        req['request'] = kwargs['urlpath']
        req['nonce'] = str(int(1000 * time.time()))

        js = json.dumps(req)
        data = base64.standard_b64encode(js.encode('utf8'))

        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha384)
        signature = h.hexdigest()
        headers = {"X-BFX-APIKEY": self.key,
                   "X-BFX-SIGNATURE": signature,
                   "X-BFX-PAYLOAD": data}
        url = self.uri + kwargs['urlpath']

        return url, {'headers': headers}

