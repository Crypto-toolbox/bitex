"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import requests
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
        print("URI is: ", uri)

    def load_key(self, path):
        """
        Load key and secret from file.
        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()

    def sign(self, *args, **kwargs):
        """
        Dummy Signature creation method. Override this in child.
        Returned dict must have keywords usable by requests.get or requests.post
        """

        return kwargs

    def query(self, endpoint, post=False, authenticate=False, *args, **kwargs):
        """
        Queries exchange using given data. Defaults to unauthenticated GET query.
        """
        print(endpoint, post, authenticate, args, kwargs)
        if self.apiversion:
            urlpath = '/' + self.apiversion + '/' + endpoint
        else:
            urlpath = '/' + endpoint

        if authenticate:  # Pass all locally vars to sign(); Sorting left to children
            kwargs['urlpath'] = urlpath
            kwargs = self.sign(endpoint, *args, **kwargs)

        url = self.uri + urlpath
        print(url)
        request_method = requests.post if post else requests.get

        r = request_method(url, timeout=5, **kwargs)

        return r



