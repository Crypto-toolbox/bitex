# Import Built-ins
import logging
import hashlib
import hmac
import base64
import urllib
import urllib.parse


# Import Third-Party

# Import Homebrew
from bitex.base import RESTAPI
log = logging.getLogger(__name__)


class KrakenREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://api.kraken.com' if not addr else addr
        version = '0' if not version else version
        super(KrakenREST, self).__init__(addr=addr, version=version, key=key,
                                         config=config, secret=secret,
                                         timeout=timeout)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(KrakenREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)
        # Prepare Payload
        try:
            payload = kwargs['params']
        except KeyError:
            payload = {}
        payload['nonce'] = self.nonce()

        # Generate Signature
        postdata = urllib.parse.urlencode(payload)
        encoded = (str(payload['nonce']) + postdata).encode('utf-8')
        message = (self.generate_uri(endpoint).encode('utf-8') +
                   hashlib.sha256(encoded).digest())

        sig_hmac = hmac.new(base64.b64decode(self.secret),
                            message, hashlib.sha512)
        signature = base64.b64encode(sig_hmac.digest())

        # Update request kwargs
        req_kwargs['headers'] = {'API-Key': self.key,
                                 'API-Sign': signature.decode('utf-8')}
        req_kwargs['data'] = payload

        return req_kwargs

