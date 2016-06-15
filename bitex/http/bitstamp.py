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
    def __init__(self, server_addr, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitstampHTTP, self).__init__(server_addr, api, 'Bitstamp')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(BitstampHTTP, self).send(message)

    def format_ob(self, input):
        ts = input['timestamp']
        formatted = []
        for a, b in zip(input['asks'], input['bids']):
            ask_p, ask_v = a
            bid_p, bid_v = b
            formatted.append([ts, 'Ask Price', ask_p])
            formatted.append([ts, 'Ask Vol', ask_v])
            formatted.append([ts, 'Bid Price',  bid_p])
            formatted.append([ts, 'Bid Vol', bid_v])
        return formatted

    def orderbook(self, pair, count=0):
        q = {'pair': pair}
        if count:
            q['count'] = count

        sent = time.time()
        resp = self._query('order_book/%s/' % pair)
        received = time.time()
        formatted = self.format_ob(resp)
        for i in formatted:
            self.send(super(BitstampHTTP, self)._format(pair, sent, received, *i))


if __name__ == '__main__':
    uix = BitstampHTTP(('localhost', 676))
    uix.orderbook('BTCUSD')