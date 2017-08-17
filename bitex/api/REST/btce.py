# Import Built-ins
import logging
import hashlib
import hmac
import urllib
import urllib.parse

# Import Third-Party

# Import Homebrew
from bitex.base import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class BTCEREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        version = '3' if not version else version
        addr = 'https://btc-e.com/api' if not addr else addr
        super(BTCEREST, self).__init__(addr=addr, version=version, key=key,
                                       secret=secret, timeout=timeout,
                                       config=config)
        self._nonce_counter = 0

    def nonce(self):
        self._nonce_counter += 1
        return self._nonce_counter

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(BTCEREST, self).sign_request_kwargs(endpoint,
                                                               **kwargs)
        # Prepare POST payload
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        post_params = params
        post_params.update({'nonce': nonce,
                            'method': endpoint})
        post_params = urllib.parse.urlencode(post_params)

        # Sign POST payload
        signature = hmac.new(self.secret.encode('utf-8'),
                             post_params.encode('utf-8'),
                             hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'Key': self.key, 'Sign': signature,
                                 "Content-type": "application/x-www-form-urlencoded"}

        # update url for POST;
        req_kwargs['url'] = self.addr.replace('/api', '/tapi')
        req_kwargs['data'] = post_params
        return req_kwargs
