"""
Contains all API Client sub-classes, which store exchange specific details
and feature the respective exchanges authentication method (sign_request_kwargs()).
"""
# Import Built-ins
import logging
import json
import hashlib
import hmac
import base64
import time
import urllib
import urllib.parse
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
from bitex.exceptions import IncompleteCredentialsWarning
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteCredentialConfigurationWarning


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


class BitstampREST(RESTAPI):
    def __init__(self, addr=None, user_id=None, key=None, secret=None,
                 version=None, timeout=5, config=None):
        addr = 'https://www.bitstamp.net/api' if not addr else addr
        if user_id == '':
            raise ValueError("Invalid user id - cannot be empty string! "
                             "Pass None instead!")
        version = 'v2' if not version else version
        self.user_id = user_id
        super(BitstampREST, self).__init__(addr=addr, version=version,
                                           key=key, secret=secret,
                                           timeout=timeout, config=config)

    def check_auth_requirements(self):
        try:
            super(BitstampREST, self).check_auth_requirements()
        except IncompleteCredentialsError:
            raise

        if self.user_id is None:
            raise IncompleteCredentialsError
        else:
            return

    def generate_uri(self, endpoint):
        if endpoint.startswith('api'):
            return endpoint[3:]
        else:
            return super(BitstampREST, self).generate_uri(endpoint)

    def load_config(self, fname):
        conf = super(BitstampREST, self).load_config(fname)
        try:
            self.user_id = conf['AUTH']['user_id']
        except KeyError:
            if self.user_id is None:
                warnings.warn("'user_id' not found in config!",
                              IncompleteCredentialConfigurationWarning)
        return conf

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(BitstampREST, self).sign_request_kwargs(endpoint,
                                                                   **kwargs)

        # Generate Signature
        nonce = self.nonce()
        message = nonce + self.user_id + self.key
        signature = hmac.new(self.secret.encode('utf-8'),
                             message.encode('utf-8'), hashlib.sha256)
        signature = signature.hexdigest().upper()

        # Parameters go into the data kwarg, so move it there from 'params'
        params = req_kwargs.pop('params')
        params['key'] = self.key
        params['nonce'] = nonce
        params['signature'] = signature
        req_kwargs['data'] = params

        return req_kwargs


class BittrexREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        version = 'v1.1' if not version else version
        addr = 'https://bittrex.com/api' if not addr else addr
        super(BittrexREST, self).__init__(addr=addr, version=version, key=key,
                                          secret=secret, timeout=timeout,
                                          config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """
        Bittrex requires the request address to be included as a sha512 encoded
        string in the query header. This means that the request address used for
        signing, and the actual address used to send the request (incuding order
        of parameters) needs to be identical. Hence, we must build the request
        address ourselves, instead of relying on the requests library to do it
        for us.
        """
        req_kwargs = super(BittrexREST, self).sign_request_kwargs(endpoint,
                                                                  **kwargs)

        # Prepare arguments for query request.
        try:
            params = kwargs.pop('params')
        except KeyError:
            params = {}
        nonce = self.nonce()
        uri = self.generate_uri(endpoint)
        url = self.generate_url(uri)

        # Build request address
        req_string = '?apikey=' + self.key + "&nonce=" + nonce + '&'
        req_string += urllib.parse.urlencode(params)
        request_address = url + req_string
        req_kwargs['url'] = request_address

        # generate signature
        signature = hmac.new(self.secret.encode('utf-8'),
                             request_address.encode('utf-8'),
                             hashlib.sha512).hexdigest()
        req_kwargs['headers'] = {"apisign": signature}

        return req_kwargs


class CoincheckREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://coincheck.com' if not addr else addr
        version = 'api' if not version else version
        super(CoincheckREST, self).__init__(addr=addr, version=version,
                                            key=key, secret=secret,
                                            timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(CoincheckREST, self).sign_request_kwargs(endpoint,
                                                                    **kwargs)

        # Prepare argument for signature
        try:
            params = kwargs.pop('params')
        except KeyError:
            params = {}
        nonce = self.nonce()
        params = json.dumps(params)

        # Create signature
        # sig = nonce + url + req

        data = (nonce + req_kwargs['url'] + params).encode('utf-8')
        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha256)
        signature = h.hexdigest()

        # Update headers
        req_kwargs['headers'] = {"ACCESS-KEY": self.key,
                                 "ACCESS-NONCE": nonce,
                                 "ACCESS-SIGNATURE": signature}

        return req_kwargs


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


class ITbitREST(RESTAPI):
    def __init__(self, user_id=None, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        self.userId = user_id
        version = 'v1' if not version else version
        addr = 'https://api.itbit.com' if not addr else addr

        if user_id == '':
            raise ValueError("Invalid user id - cannot be empty string! "
                             "Pass None instead!")
        self.user_id = user_id
        super(ITbitREST, self).__init__(addr=addr, version=version, key=key,
                                        secret=secret, timeout=timeout,
                                        config=config)

    def check_auth_requirements(self):
        try:
            super(ITbitREST, self).check_auth_requirements()
        except IncompleteCredentialsError:
            raise

        if self.user_id is None:
            raise IncompleteCredentialsError
        else:
            return

    def load_config(self, fname):
        conf = super(ITbitREST, self).load_config(fname)
        try:
            self.user_id = conf['AUTH']['user_id']
        except KeyError:
            warnings.warn("'user_id' not found in config!",
                          IncompleteCredentialConfigurationWarning)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Requires that the HTTP request VERB is passed along in kwargs as
        as key:value pair 'method':<Verb>; otherwise authentication will
        not work.
        """
        req_kwargs = super(ITbitREST, self).sign_request_kwargs(endpoint,
                                                                **kwargs)

        # Prepare payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        verb = kwargs['method']

        if verb in ('PUT', 'POST'):
            body = params
        else:
            body = {}

        timestamp = self.nonce()
        nonce = self.nonce()

        message = json.dumps([verb, req_kwargs['url'], body, nonce, timestamp],
                             separators=(',', ':'))
        sha256_hash = hashlib.sha256()
        nonced_message = nonce + message
        sha256_hash.update(nonced_message.encode('utf8'))
        hash_digest = sha256_hash.digest()
        hmac_digest = hmac.new(self.secret.encode('utf-8'),
                               req_kwargs['url'].encode('utf-8') + hash_digest,
                               hashlib.sha512).digest()
        signature = base64.b64encode(hmac_digest)

        # Update request kwargs header variable
        req_kwargs['headers'] = {'Authorization': self.key + ':' + signature.decode('utf8'),
                                 'X-Auth-Timestamp': timestamp,
                                 'X-Auth-Nonce': nonce,
                                 'Content-Type': 'application/json'}
        return req_kwargs


class OKCoinREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        version = 'v1' if not version else version
        addr = 'https://www.okcoin.com/api' if not addr else addr
        super(OKCoinREST, self).__init__(addr=addr, version=version,
                                         key=key, secret=secret, config=config,
                                         timeout=timeout)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """ OKCoin requires the parameters in the signature string and url to
        be appended in alphabetical order. This means we cannot rely on urllib's
        encode() method and need to do this ourselves.
        """

        req_kwargs = super(OKCoinREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)
        # Prepare payload arguments
        nonce = self.nonce()
        try:
            payload = kwargs['params']
        except KeyError:
            payload = {}
        payload['api_key'] = self.key

        # Create the signature from payload and add it to params
        encoded_payload = ''
        for k in sorted(payload.keys()):
            encoded_payload += k + '=' + payload[k] + '&'
        sign = encoded_payload + 'secret_key=' + self.secret
        hash_sign = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()

        # create params dict for body
        body = {'api_key': self.key, 'sign': hash_sign}

        # Update req_kwargs keys
        req_kwargs['data'] = urllib.parse.urlencode(body)
        req_kwargs['headers'] = {"Content-type": 'application/x-www-form-urlencoded'}
        #req_kwargs['url'] = encoded_url
        return req_kwargs


class BTCEREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        version = '3' if not version else version
        addr = 'https://btc-e.com/api' if not addr else addr
        super(BTCEREST, self).__init__(addr=addr, version=version, key=key,
                                       secret=secret, timeout=timeout,
                                       config=config)

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
        post_params = '?' + urllib.parse.urlencode(post_params)

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


class CCEXREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://c-cex.com/t' if not addr else addr

        super(CCEXREST, self).__init__(addr=addr, version=version, key=key,
                                       secret=secret, timeout=timeout,
                                       config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(CCEXREST, self).sign_request_kwargs(endpoint,
                                                               **kwargs)

        # Prepare Payload arguments
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        params['apikey'] = self.key
        params['nonce'] = nonce
        post_params = params
        post_params.update({'nonce': nonce, 'a': endpoint})
        url_params = urllib.parse.urlencode(post_params)
        url = self.addr + '/api.html?' + url_params

        # generate signature
        sig = hmac.new(self.secret.encode('utf-8'), url.encode('utf-8'),
                       hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'apisign': sig}
        req_kwargs['url'] = url

        return req_kwargs


class CryptopiaREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        addr = 'https://www.cryptopia.co.nz/api' if not addr else addr
        super(CryptopiaREST, self).__init__(addr=addr, version=version, key=key,
                                            secret=secret, timeout=timeout,
                                            config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(CryptopiaREST, self).sign_request_kwargs(endpoint,
                                                                    **kwargs)

        # Prepare POST Payload arguments
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        post_data = json.dumps(params)

        # generate signature
        md5 = hashlib.md5()
        md5.update(post_data.encode('utf-8'))
        request_content_b64_string = base64.b64encode(md5.digest()).decode('utf-8')
        signature = (self.key + 'POST' +
                     urllib.parse.quote_plus(req_kwargs['url']).lower() +
                     nonce + request_content_b64_string)

        hmac_sig = base64.b64encode(hmac.new(base64.b64decode(self.secret),
                                             signature.encode('utf-8'),
                                             hashlib.sha256).digest())
        header_data = 'amx' + self.key + ':' + hmac_sig.decode('utf-8') + ':' + nonce

        # Update req_kwargs keys
        req_kwargs['headers'] = {'Authorization': header_data,
                                 'Content-Type': 'application/json; charset=utf-8'}
        req_kwargs['data'] = post_data

        return req_kwargs


class GeminiREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://api.gemini.com' if not addr else addr
        version = 'v1' if not version else version
        super(GeminiREST, self).__init__(addr=addr, version=version, key=key,
                                         secret=secret, timeout=timeout,
                                         config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(GeminiREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)

        # Prepare Payload
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        payload = params
        payload['nonce'] = nonce
        payload['request'] = self.generate_uri(endpoint)
        payload = base64.b64encode(json.dumps(payload))

        # generate signature
        sig = hmac.new(self.secret, payload, hashlib.sha384).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'X-GEMINI-APIKEY': self.key,
                                 'X-GEMINI-PAYLOAD': payload,
                                 'X-GEMINI-SIGNATURE': sig}
        return req_kwargs


class YunbiREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        version = 'v2' if not version else version
        addr = 'https://yunbi.com/api' if not addr else addr
        super(YunbiREST, self).__init__(addr=addr, version=version, key=key,
                                        secret=secret, timeout=timeout,
                                        config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Requires that the HTTP request VERB is passed along in kwargs as
        as key:value pair 'method':<Verb>; otherwise authentication will
        not work.
        """
        req_kwargs = super(YunbiREST, self).sign_request_kwargs(endpoint,
                                                                **kwargs)
        # prepare Payload arguments
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        params['tonce'] = nonce
        params['access_key'] = self.key
        post_params = urllib.parse.urlencode(params)
        msg = '%s|%s|%s' % (kwargs['method'], self.generate_uri(endpoint),
                            post_params)

        # generate signature
        sig = hmac.new(self.secret, msg, hashlib.sha256).hexdigest()

        # update req_kwargs keys
        req_kwargs['url'] += post_params + '&signature=' + sig

        return req_kwargs


class RockTradingREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        version = 'v1' if not version else version
        addr = 'https://api.therocktrading.com' if not addr else addr
        super(RockTradingREST, self).__init__(addr=addr, version=version,
                                              key=key, secret=secret,
                                              timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(RockTradingREST, self).sign_request_kwargs(endpoint,
                                                                      **kwargs)
        # Prepare Payload arguments
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        payload = params
        payload['nonce'] = int(nonce)
        #payload['request'] = self.generate_uri(endpoint)

        # generate signature
        msg = nonce + req_kwargs['url']
        sig = hmac.new(self.secret.encode(), msg.encode(),
                       hashlib.sha512).hexdigest()

        # Update req_kwargs keys
        req_kwargs['headers'] = {'X-TRT-KEY': self.key, 'X-TRT-Nonce': nonce,
                                 'X-TRT-SIGN': sig,
                                 'Content-Type': 'application/json'}
        req_kwargs['json'] = payload
        return req_kwargs


class PoloniexREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        addr = 'https://poloniex.com' if not addr else addr
        super(PoloniexREST, self).__init__(addr=addr, version=version,
                                           key=key, secret=secret,
                                           timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(PoloniexREST, self).sign_request_kwargs(endpoint,
                                                                   **kwargs)

        # Prepare Payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        params['nonce'] = self.nonce()
        params['command'] = endpoint
        payload = params

        # generate signature
        msg = urllib.parse.urlencode(payload).encode('utf-8')
        sig = hmac.new(self.secret.encode('utf-8'), msg,
                       hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'Key': self.key, 'Sign': sig}
        req_kwargs['data'] = params
        req_kwargs['url'] = self.addr + '/tradingApi'

        return req_kwargs


class QuoineREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        addr = 'https://api.quoine.com/' if not addr else addr
        version = '2' if not version else version
        super(QuoineREST, self).__init__(addr=addr, version=version,
                                         key=key, secret=secret, config=config,
                                         timeout=timeout)

    def generate_uri(self, endpoint):
        """The Quoine Api requires the API version to be designated in each
        requests's header as {'X-Quoine-API-Version': 2}, instead of adding it
        to the URL. Hence, we need to adapt generate_uri.
        """
        return endpoint

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(QuoineREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)

        # Prepare Payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        path = endpoint + urllib.parse.urlencode(params)
        msg = {'path': path, 'nonce': self.nonce(), 'token_id': self.key}

        # generate signature
        signature = jwt.encode(msg, self.secret, algorithm='HS256')

        req_kwargs['headers'] = {'X-Quoine-API-Version': self.version,
                                 'X-Quoine-Auth': signature,
                                 'Content-Type': 'application/json'}
        return req_kwargs


class QuadrigaCXREST(RESTAPI):
    def __init__(self, key=None, secret=None, client_id=None, version=None,
                 addr=None, timeout=5, config=None):

        version = 'v2' if not version else version
        addr = 'https://api.quadrigacx.com' if not addr else addr

        if client_id == '':
            raise ValueError("Invalid client id - cannot be empty string! "
                             "Pass None instead!")
        self.client_id = client_id
        super(QuadrigaCXREST, self).__init__(addr=addr, version=version,
                                             key=key, secret=secret,
                                             timeout=timeout, config=config)

    def check_auth_requirements(self):
        try:
            super(QuadrigaCXREST, self).check_auth_requirements()
        except IncompleteCredentialsError:
            raise

        if self.client_id is None:
            raise IncompleteCredentialsError
        else:
            return

    def load_config(self, fname):
        conf = super(QuadrigaCXREST, self).load_config(fname)
        try:
            self.client_id = conf['AUTH']['client_id']
        except KeyError:
            warnings.warn("'client_id' not found in config!",
                          IncompleteCredentialConfigurationWarning)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(QuadrigaCXREST, self).sign_request_kwargs(endpoint,
                                                                     **kwargs)

        # Prepare Payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        nonce = self.nonce()
        msg = nonce + self.client_id + self.key

        # generate signature
        signature = hmac.new(self.secret.encode(encoding='utf-8'),
                             msg.encode(encoding='utf-8'),
                             hashlib.sha256).hexdigest()

        # update req_kwargs keys
        req_kwargs['json'] = {'key': self.key, 'signature': signature,
                                 'nonce': nonce}
        req_kwargs['data'] = params
        return req_kwargs


class HitBTCREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        version = '1' if not version else version
        addr = 'http://api.hitbtc.com/api' if not addr else addr
        super(HitBTCREST, self).__init__(addr=addr, version=version,
                                         key=key, secret=secret,
                                         timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(HitBTCREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)

        # prepare Payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        nonce = self.nonce()
        params['nonce'] = nonce
        params['apikey'] = self.key
        path = self.generate_uri(endpoint) + '?' + urllib.parse.urlencode(params)

        # generate signature
        signature = hmac.new(self.secret.encode(encoding='utf-8'),
                             path.encode(encoding='utf-8'),
                             hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'Api-signature': signature}
        req_kwargs['url'] = self.generate_url(path)

        return req_kwargs


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
