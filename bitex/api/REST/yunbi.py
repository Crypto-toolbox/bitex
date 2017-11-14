"""Yunbi REST API backend.

Documentation available at:
    https://yunbi.com/documents/api/v2
"""
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


class YunbiREST(RESTAPI):
    """Yunbi REST API class."""

    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        """Initialize the class instance."""
        version = 'v2' if not version else version
        addr = 'https://yunbi.com/api' if not addr else addr
        super(YunbiREST, self).__init__(addr=addr, version=version, key=key,
                                        secret=secret, timeout=timeout,
                                        config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Sign the reuqest.

        Requires that the HTTP request VERB is passed along in kwargs as
        as key:value pair 'method':<Verb>; otherwise authentication will
        fail.
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
