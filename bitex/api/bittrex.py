"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging
import hashlib
import urllib
import urllib.parse
import time
import hmac
# Import Third-Party

# Import Homebrew
from bitex.api.api import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class API(RESTAPI):
    def __init__(self, key='', secret='', api_version='v1.1',
                 url='https://bittrex.com/api'):
        super(API, self).__init__(url, api_version=api_version, key=key,
                                  secret=secret)

    def sign(self, *args, **kwargs):
        urlpath = self.uri + '/' + kwargs['urlpath']

        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        nonce = str(int(time.time() * 1000))

        req_string = urlpath + '?apikey=' + self.key + "&nonce=" + nonce + '&'
        req_string += urllib.parse.urlencode(params)

        headers = {"apisign": hmac.new(self.secret.encode(), req_string.encode(),
                                       hashlib.sha512).hexdigest()}

        return req_string, {'headers': headers, 'params': {}}
