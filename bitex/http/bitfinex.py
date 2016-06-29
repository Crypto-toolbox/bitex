"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import socket
import time
import json

# Import Homebrew
from bitex.api.bitfinex import API
from bitex.http.client import Client


log = logging.getLogger(__name__)


class BitfinexHTTP(Client):
    def __init__(self, server_addr, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitfinexHTTP, self).__init__(server_addr, api, 'Bitfinex')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(BitfinexHTTP, self).send(message)

    def order_book(self, pair, limit_orders=50, aggregrate=True):
        q = {'limit_asks': limit_orders, 'limit_bids': limit_orders}
        if not aggregrate:
            q['group'] = 0
        return self._query('/book/%s/' % pair, q)

    def ticker(self, pair):
        return self._query('/pubticker/%s' % pair)


if __name__ == '__main__':
    uix = BitfinexHTTP(('localhost', 6666), 'BTCUSD')
    uix.orderbook('BTCUSD')