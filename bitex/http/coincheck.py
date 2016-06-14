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
from bitex.http.client import Client
from bitex.api.coincheck import API

log = logging.getLogger(__name__)


class CoincheckHTTP(Client):
    def __init__(self, server_addr, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(CoincheckHTTP, self).__init__(server_addr, api, 'Coincheck')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(CoincheckHTTP, self).send(message)

    def format_ob(self, input):
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
        resp = self._query('order_books', q)
        received = time.time()
        formatted = self.format_ob(resp)
        for i in formatted:
            self.send(super(CoincheckHTTP, self)._format(pair, sent, received, *i))



if __name__ == '__main__':
    uix = CoincheckHTTP(('localhost', 6666), 'BTCJPY')
    uix.orderbook('BTCJPY')
