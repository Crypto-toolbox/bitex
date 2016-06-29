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
from bitex.api.gdax import API
from bitex.http.client import Client

# Import Homebrew

log = logging.getLogger(__name__)


class GdaxHTTP(Client):
    def __init__(self, server_addr, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(GdaxHTTP, self).__init__(server_addr, api, 'GDAX')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(GdaxHTTP, self).send(message)

    def order_book(self, pair):
        q = {'pair': pair}
        return self._query('/products/%s/book' % pair, q)

    def ticker(self, pair):
        return self._query('/%s/ticker' % pair)

if __name__ == '__main__':
    uix = GdaxHTTP(('localhost', 6666))
    print(uix.order_book('BTC-USD'))
    print(uix.ticker('BTC-USD'))
