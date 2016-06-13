"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
from socket import AF_INET, SOCK_DGRAM, socket
# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


class Client:
    """
    Base Class for http clients. One client per pair!
    """
    def __init__(self, receiver_addr, exchange, name, pair):
        """
        Base Class for http clients
        :param receiver_addr: tuple, ex ('localhost', 6666)
        :param exchange: API Class
        :param name: str, name of exchange
        :param pair: str, pair as used in querying exchange.
        """
        self._receiver = receiver_addr
        self._exchange = exchange
        self._name = name
        self._pair = pair

    def send(self, message):
        """
        Send message to self._receiver
        :param message: bytes
        :return: None
        """
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.sendto(message, self._receiver)

    def run(self):
        pass

    def _format_ob(self, ls):
        """
        adds pair and exchange to list, converts to string and sends it out.
        :param ls: list or field values
        :return: str
        """
        ts_sent, ts_received, *rest = ls
        new = [ts_sent, ts_received, self._pair, self._name, *rest]
        return '\t'.join(new)

