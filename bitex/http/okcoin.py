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

    def format_ob(self, input):
        formatted = []
        for a, b in zip(input['asks'], input['bids']):
            ask_p, ask_v = a
            bid_p, bid_v = b
            formatted.append([None, 'Ask Price', ask_p])
            formatted.append([None, 'Ask Vol', ask_v])
            formatted.append([None, 'Bid Price',  bid_p])
            formatted.append([None, 'Bid Vol', bid_v])
        return formatted

    def orderbook(self, pair):
        q = {'pair': pair}

        sent = time.time()
        resp = self._query('depth.do', q)
        received = time.time()
        formatted = self.format_ob(resp, pair)
        for i in formatted:
            self.send(super(OKCoinHTTP, self)._format(pair, sent, received, *i))

    def ticker(self, pair):
        return self._query('/ticker', {'symbol': pair})

if __name__ == '__main__':
    uix = OKCoinHTTP(('localhost', 6666))
    uix.orderbook('BTCUSD')
