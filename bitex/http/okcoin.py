"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import socket
import time
import json

# Import Third-Party


# Import Homebrew
from bitex.api.okcoin import API
from bitex.http.client import Client

log = logging.getLogger(__name__)


class OKCoinHTTP(Client):
    def __init__(self, server_addr, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(OKCoinHTTP, self).__init__(server_addr, api, 'OKCoin')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(OKCoinHTTP, self).send(message)

    def order_book(self, pair):
        q = {'pair': pair}
        return self._query('depth.do', q)

    def ticker(self, pair):
        return self._query('/ticker', {'pair':pair})

if __name__ == '__main__':
    uix = OKCoinHTTP(('localhost', 6666))
    uix.orderbook('BTCUSD')
