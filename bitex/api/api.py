"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import requests
import time
# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


class RESTAPI:

    def __init__(self, uri, api_version='', key='', secret=''):
        """
        Base Class for REST API connections.
        """
        self.key = key
        self.secret = secret
        self.uri = uri
        self.apiversion = api_version
        self.req_methods = {'POST': requests.post, 'PUT': requests.put,
                            'GET': requests.get, 'DELETE': requests.delete,
                            'PATCH': requests.patch}
        log.debug("Initialized RESTAPI for URI: %s; "
                  "Will request on API version: %s" %
                  (self.uri, self.apiversion))

    def load_key(self, path):
        """
        Load key and secret from file.
        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()

    def nonce(self):
        return str(int(1000 * time.time()))

    def sign(self, url, endpoint, endpoint_path, method_verb, *args, **kwargs):
        """
        Dummy Signature creation method. Override this in child.
        Returned dict must have keywords usable by requests.get or requests.post
        URL is required to be returned, as some Signatures use the url for
        sig generation, and api calls made must match the address exactly.
        """
        url = self.uri

        return url, {'params': {'test_param': "authenticated_chimichanga"}}

    def query(self, method_verb, endpoint, authenticate=False,
              *args, **kwargs):
        """
        Queries exchange using given data. Defaults to unauthenticated GET query.
        """
        request_method = self.req_methods[method_verb]

        if self.apiversion:
            endpoint_path = '/' + self.apiversion + '/' + endpoint
        else:
            endpoint_path = '/' + endpoint

        url = self.uri + endpoint_path
        if authenticate:  # sign off kwargs and url before sending request
            url, request_kwargs = self.sign(url, endpoint, endpoint_path,
                                            method_verb, *args, **kwargs)
        else:
            request_kwargs = kwargs
        log.debug("Making request to: %s, kwargs: %s" % (url, request_kwargs))
        r = request_method(url, timeout=5, **request_kwargs)
        log.debug("Made %s request made to %s, with headers %s and body %s. "
                  "Status code %s" %
                  (r.request.method, r.request.url, r.request.headers,
                   r.request.body, r.status_code))
        return r







