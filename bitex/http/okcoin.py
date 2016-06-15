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

    def format_ob(self, input, pair):
        ask_p, ask_v = input['asks'][0]
        bid_p, bid_v = input['bids'][0]
        formatted = [[None, 'Ask Price', ask_p],
                     [None, 'Ask Vol', ask_v],
                     [None, 'Bid Price',  bid_p],
                     [None, 'Bid Vol', bid_v]]
        return formatted

    def orderbook(self, pair):
        q = {'pair': pair}

        sent = time.time()
        resp = self._query('depth.do', q)
        received = time.time()
        formatted = self.format_ob(resp, pair)
        for i in formatted:
            self.send(super(OKCoinHTTP, self)._format(pair, sent, received, *i))


if __name__ == '__main__':
    uix = OKCoinHTTP(('localhost', 6666))
    uix.orderbook('BTCUSD')
