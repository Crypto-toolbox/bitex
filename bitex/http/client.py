"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import json
from socket import AF_INET, SOCK_DGRAM, socket
# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


class Client:
    """
    Base Class for http clients. One client per pair!
    """
    def __init__(self, receiver_addr, api, name):
        """
        Base Class for http clients
        :param receiver_addr: tuple, ex ('localhost', 6666)
        :param api: API Class
        :param name: str, name of exchange
        :param pair: str, pair as used in querying exchange.
        """
        self._receiver = receiver_addr
        self._api = api
        self._name = name

    def send(self, message):
        """
        Send message to self._receiver
        :param message: bytes
        :return: None
        """
        print(message)

    def _query(self, method, q={}, private=False):

        if private:
            resp = self._api.query_private(method, q)
        else:
            resp = self._api.query_public(method, q)
        return resp

    def _format(self, pair, sent, received, *ls):
        """
        adds pair and exchange to list, converts to string and sends it out.
        :param sent: timestamp
        :param received: timestamp
        :param ls: list or field values
        :return: str
        """
        new = [sent, received, pair, self._name, *ls]

        return json.dumps(new)

