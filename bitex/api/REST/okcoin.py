# Import Built-ins
import logging
import logging
import hashlib


# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class OKCoinREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        version = 'v1' if not version else version
        addr = 'https://www.okcoin.com/api' if not addr else addr
        super(OKCoinREST, self).__init__(addr=addr, version=version,
                                         key=key, secret=secret, config=config,
                                         timeout=timeout)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """
        OKCoin requires the parameters in the signature string and url to
        be appended in alphabetical order. This means we cannot rely on urllib's
        encode() method and need to do this ourselves.
        """

        req_kwargs = super(OKCoinREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)
        # Prepare payload arguments
        nonce = self.nonce()
        try:
            payload = req_kwargs.pop('params')
        except KeyError:
            payload = {}
        payload['api_key'] = self.key

        # Create the signature from payload and add it to params
        encoded_params = ''
        for k in sorted(payload.keys()):
            encoded_params += str(k) + '=' + str(payload[k]) + '&'
        sign = encoded_params + 'secret_key=' + self.secret
        hash_sign = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()

        # create params dict for body
        body = {'api_key': self.key, 'sign': hash_sign}

        # Update req_kwargs keys
        req_kwargs['data'] = body
        req_kwargs['headers'] = {"contentType": 'application/x-www-form-urlencoded'}
        req_kwargs['url'] = self.generate_url(self.generate_uri(endpoint + '?' + encoded_params[:-1]))
        return req_kwargs
