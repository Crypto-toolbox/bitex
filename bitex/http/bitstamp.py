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
from bitex.api.bitstamp import API
from bitex.http.client import Client


log = logging.getLogger(__name__)


class BitstampHTTP(Client):
    def __init__(self, server_addr, pair, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitstampHTTP, self).__init__(server_addr, api, 'Bitstamp', pair)

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(BitstampHTTP, self).send(message)

    def format_ob(self, input):
        ts = input['timestamp']
        ask_p, ask_v = input['asks'][0]
        bid_p, bid_v = input['bids'][0]

        formatted = [[ts, 'Ask Price', ask_p],
                     [ts, 'Ask Vol', ask_v],
                     [ts, 'Bid Price', bid_p],
                     [ts, 'Bid Vol', bid_v]]
        return formatted

    def query_ob(self, count=0):
        q = {'pair': self._pair}
        if count:
            q['count'] = count

        sent = time.time()
        resp = self._query('order_book/btcusd/')
        received = time.time()
        formatted = self.format_ob(resp)
        for i in formatted:
            self.send(super(BitstampHTTP, self)._format(sent, received, *i))


if __name__ == '__main__':
    uix = BitstampHTTP(('localhost', 676), 'BTCUSD')
    uix.query_ob()