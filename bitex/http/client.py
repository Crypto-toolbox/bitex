"""
Task:
Parent class for all APIs. Stores API, exchange name and handles
calls to the API via the query() method.
"""

# Import Built-Ins
import logging
import requests

# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


class Client:
    """
    Base Class for http clients.
    """
    def __init__(self, api, name):
        """
        Base Class for http clients
        :param api: API Class
        :param name: str, name of exchange
        :param pair: str, pair as used in querying exchange.
        """
        self._api = api
        self._name = name
        self._methods = {'POST': requests.post, 'PUT': requests.put,
                         'GET': requests.get, 'DELETE': requests.delete,
                         'PATCH': requests.patch}

    def query(self, endpoint, req_type='GET', authenticate=False, *args, **kwargs):

        if req_type not in self._methods:
            raise ValueError("req_type contains unknown request type!")

        return self._api.query(endpoint, request_method=self._methods[req_type],
                               authenticate=authenticate, *args, **kwargs)


