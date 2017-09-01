# Import Built-ins
import logging
import json
import hashlib
import hmac
import base64

# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI

log = logging.getLogger(__name__)


class BitfinexREST(RESTAPI):
    def __init__(self, addr=None, key=None, secret=None,
                 version=None, config=None, timeout=None):
        addr = 'https://api.bitfinex.com' if not addr else addr
        version = 'v1' if not version else version
        super(BitfinexREST, self).__init__(addr=addr, version=version, key=key,
                                           secret=secret, timeout=timeout,
                                           config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(BitfinexREST, self).sign_request_kwargs(endpoint,
                                                                   **kwargs)

        # Parameters go into headers, so pop params key and generate signature
        params = req_kwargs.pop('params')
        params['request'] = self.generate_uri(endpoint)
        params['nonce'] = self.nonce()

        # convert to json, encode and hash
        js = json.dumps(params)
        data = base64.standard_b64encode(js.encode('utf8'))

        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha384)
        signature = h.hexdigest()

        # Update headers and return
        req_kwargs['headers'] = {"X-BFX-APIKEY": self.key,
                                 "X-BFX-SIGNATURE": signature,
                                 "X-BFX-PAYLOAD": data}

        return req_kwargs
