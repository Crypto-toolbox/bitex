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


class BterREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'http://data.bter.com/api2' if not addr else addr
        version = '1' if not version else version
        super(BterREST, self).__init__(addr=addr, version=version, key=key,
                                       secret=secret, timeout=timeout,
                                       config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(BterREST, self).sign_request_kwargs(endpoint,
                                                               **kwargs)
        # prepare Payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        nonce = self.nonce()
        kwargs['nonce'] = nonce
        encoded_params = urllib.parse.urlencode(params)
        url = self.generate_url(self.generate_uri(endpoint) + encoded_params)

        # generate signature
        signature = hmac.new(self.secret.encode(encoding='utf-8'),
                             encoded_params.encode(encoding='utf-8'),
                             hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'Key': signature, 'Sign': signature}
        req_kwargs['url'] = url

        return req_kwargs
