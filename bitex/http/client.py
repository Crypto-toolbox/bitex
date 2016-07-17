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


class Client:
    """
    Base Class for http clients. One client per pair!
    """
    def __init__(self, api, name):
        """
        Base Class for http clients
        :param receiver_addr: tuple, ex ('localhost', 6666)
        :param api: API Class
        :param name: str, name of exchange
        :param pair: str, pair as used in querying exchange.
        """
        self._api = api
        self._name = name

    def query(self, method, post=False, authenticate=False, *args, **kwargs):
        if post:
            request_method = requests.post
        else:
            request_method = requests.get
        return self._api.query(method, request_method=request_method,
                               authenticate=authenticate, *args, **kwargs)

    def _format(self, sent, received, pair, *ls):
        """
        adds pair and exchange to list, converts to string and sends it out.
        :param sent: timestamp
        :param received: timestamp
        :param ls: list or field values
        :return: list
        """
        new = [sent, received, pair, self._name, *ls]

        return new

