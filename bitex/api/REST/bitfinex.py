"""Bitfinex REST API backend.

Documentation available at:
    https://docs.bitfinex.com/docs
"""
# pylint: disable=too-many-arguments
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
    """Bitfinex REST API class."""

    def __init__(self, addr=None, key=None, secret=None,
                 version=None, config=None, timeout=None):
        """Initialize the class instance."""
        addr = 'https://api.bitfinex.com' if not addr else addr
        version = 'v1' if not version else version
        super(BitfinexREST, self).__init__(addr=addr, version=version, key=key,
                                           secret=secret, timeout=timeout,
                                           config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Sign the request."""
        req_kwargs = super(BitfinexREST, self).sign_request_kwargs(endpoint,
                                                                   **kwargs)

        # Parameters go into headers, so pop params key and generate signature
        params = req_kwargs.pop('params')

        params['request'] = self.generate_uri(endpoint)
        params['nonce'] = self.nonce()

        # convert to json, encode and hash
        payload = json.dumps(params)
        data = base64.standard_b64encode(payload.encode('utf8'))

        hmac_sig = hmac.new(self.secret.encode('utf8'), data, hashlib.sha384)
        signature = hmac_sig.hexdigest()

        # Update headers and return
        req_kwargs['headers'] = {"X-BFX-APIKEY": self.key,
                                 "X-BFX-SIGNATURE": signature,
                                 "X-BFX-PAYLOAD": data,
                                 "Content-Type": "application/json",
                                 "Accept": "application/json"}

        return req_kwargs
