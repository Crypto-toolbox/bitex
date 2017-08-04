# Import Built-ins
import logging
import hashlib
import hmac
import base64
import time
import warnings

# Import Third-Party
from requests.auth import AuthBase
try:
    import pyjwt as jwt
    jwt = True
except ImportError:
    jwt = False

# Import Homebrew
from bitex.base import RESTAPI
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteCredentialConfigurationWarning


log = logging.getLogger(__name__)


class GDAXAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key.encode('utf-8')
        self.secret_key = secret_key.encode('utf-8')
        self.passphrase = passphrase.encode('utf-8')

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + request.method + request.path_url +
                   (request.body or ''))
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({'CB-ACCESS-SIGN': signature_b64,
                                'CB-ACCESS-TIMESTAMP': timestamp,
                                'CB-ACCESS-KEY': self.api_key,
                                'CB-ACCESS-PASSPHRASE': self.passphrase,
                                'Content-Type': 'application/json'})
        return request


class GDAXREST(RESTAPI):
    def __init__(self, passphrase=None, key=None, secret=None, version=None,
                 addr=None, config=None, timeout=5):
        if passphrase == '':
            raise ValueError("Invalid user id - cannot be empty string! "
                             "Pass None instead!")
        self.passphrase = passphrase
        addr = 'https://api.gdax.com' if not addr else addr

        super(GDAXREST, self).__init__(addr=addr, version=version, key=key,
                                       secret=secret, timeout=timeout,
                                       config=config)

    def check_auth_requirements(self):
        try:
            super(GDAXREST, self).check_auth_requirements()
        except IncompleteCredentialsError:
            raise

        if self.passphrase is None:
            raise IncompleteCredentialsError
        else:
            return

    def load_config(self, fname):
        conf = super(GDAXREST, self).load_config(fname)
        try:
            self.passphrase = conf['AUTH']['passphrase']
        except KeyError:
            warnings.warn("'passphrase' not found in config!",
                          IncompleteCredentialConfigurationWarning)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(GDAXREST, self).sign_request_kwargs(endpoint,
                                                               **kwargs)
        req_kwargs['auth'] = GDAXAuth(self.key, self.secret, self.passphrase)

        try:
            req_kwargs['json'] = kwargs['params']
        except KeyError:
            pass

        return req_kwargs

