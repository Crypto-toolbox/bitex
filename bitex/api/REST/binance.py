"""Binance REST API backend.

Documentation available at:
    https://github.com/binance-exchange/binance-official-api-docs/
"""
# pylint: disable=too-many-arguments
# Import Built-ins
import logging
import hashlib
import hmac
import time
import urllib
import urllib.parse

# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI

log = logging.getLogger(__name__)


class BinanceREST(RESTAPI):
    """Binance REST API class."""

    def __init__(self, key=None, secret=None, version=None, addr=None, timeout=None, config=None):
        """Initialize the class instance."""
        addr = 'https://api.binance.com'
        # We force version to None here as different endpoints require different versions,
        # so the interface will have to define the version as part of the endpoint.
        super(BinanceREST, self).__init__(addr=addr, version=None, key=key, secret=secret,
                                          timeout=timeout, config=config)

    def private_query(self, method_verb, endpoint, **request_kwargs):
        """
        Query a private API endpoint requiring signing of the request.

        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param endpoint: str, API Endpoint
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        self.check_auth_requirements()
        request_kwargs = self.sign_request_kwargs(endpoint, method_verb, **request_kwargs)
        return self._query(method_verb, **request_kwargs)

    def sign_request_kwargs(self, endpoint, method_verb=None, **kwargs):
        """Sign the request."""
        uri = self.generate_uri(endpoint)
        url = self.generate_url(uri)
        req_kwargs = {'url': url, 'headers': {'X-MBX-APIKEY': self.key.encode('utf-8')}}

        params = kwargs.pop('params', {})
        params['timestamp'] = str(int(time.time() * 1000))
        req_string = urllib.parse.urlencode(params)
        params['signature'] = hmac.new(self.secret.encode('utf-8'), req_string.encode('utf-8'),
                                       hashlib.sha256).hexdigest()

        # WAPI params must be in the querystring, see https://github.com/ccxt/ccxt/issues/320
        req_kwargs['params'] = params

        return req_kwargs
