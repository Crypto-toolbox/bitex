# Import Built-ins
import logging
import hashlib
import hmac
import urllib
import urllib.parse


# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class VaultoroREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://api.vaultoro.com' if not addr else addr
        super(VaultoroREST, self).__init__(addr=addr, version=version,
                                           key=key, secret=secret,
                                           timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(VaultoroREST, self).sign_request_kwargs(endpoint,
                                                                   **kwargs)

        # prepare Payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        nonce = self.nonce()
        params['nonce'] = nonce
        params['apikey'] = self.key
        url = self.generate_url('/' + endpoint + '?' + urllib.parse.urlencode(params))

        # generate signature
        signature = hmac.new(self.secret.encode(encoding='utf-8'),
                             url.encode(encoding='utf-8'),
                             hashlib.sha256).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'X-Signature': signature}
        req_kwargs['url'] = url
        return req_kwargs
