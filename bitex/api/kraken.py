"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import time
import hashlib
import hmac
import base64
import requests
import urllib.request, urllib.parse, urllib.error
import http.client

# Import Third-Party

# Import Homebrew
from bitex.api.api import RESTAPI


class API(RESTAPI):
    def __init__(self, key='', secret='', api_version='0',
                 url='https://api.kraken.com'):
        super(API, self).__init__(url, api_version=api_version,
                          key=key, secret=secret)

    def sign(self, method, *args, **kwargs):
        try:
            req = kwargs['params']
        except KeyError:
            req = {}

        req['nonce'] = int(1000*time.time())
        postdata = urllib.parse.urlencode(req)

        # Unicode-objects must be encoded before hashing
        encoded = (str(req['nonce']) + postdata).encode()
        message = kwargs['urlpath'].encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        headers = {
            'API-Key': self.key,
            'API-Sign': sigdigest.decode()
        }

        return {'data': req, 'headers': headers}