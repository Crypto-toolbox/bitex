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

    def load_key(self, path):
        """
        Load key and secret from file.
        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()

    def sign(self, *args, **kwargs):
        """
        Dummy Signature creation method. Override this in child. Must return
        tuple of request and headers (either can be empty)
        """
        req = {}
        headers = {}
        auth = {}
        return req, headers, auth

    def _query(self, urlpath, post, req={}, headers={}):
        """
        Sends request to api, using given args.
        """
        url = self.uri + urlpath
        print(url, req)

        if post:
            r = requests.post(url, params=req, headers=headers)
        else:
            r = requests.get(url, params=req, headers=headers)
        return r

    def query_public(self, endpoint, req={}, headers={}, post=False):
        """
        API queries that do not require a valid key/secret pair. Default uses
        GET
        """
        urlpath = '/' + self.apiversion + '/' + endpoint
        return self._query(urlpath, post, req, headers)

    def query_private(self, endpoint, req={}, post=True, *args, **kwargs):
        """
        API queries that require a valid key/secret pair. Default uses POST
        """
        if self.apiversion:
            urlpath = '/' + self.apiversion + '/' + endpoint
        else:
            urlpath = '/' + endpoint

        req, headers, auth = self.sign(*args, req=req, endpoint=endpoint,
                                 urlpath=urlpath, post=post, **kwargs)
        return self._query(urlpath, req=req, post=post, headers=headers,
                           auth=auth)


