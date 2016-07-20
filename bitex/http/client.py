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

    def query(self, method, req_type='GET', authenticate=False, *args, **kwargs):
        request_method = {'POST': requests.post, 'PUT': requests.put,
                          'GET': requests.get, 'DELETE': requests.delete,
                          'PATCH': requests.patch}
        if req_type not in request_method.keys():
            raise ValueError("req_type contains unknown request type!")

        return self._api.query(method, request_method=request_method[req_type],
                               authenticate=authenticate, *args, **kwargs)


