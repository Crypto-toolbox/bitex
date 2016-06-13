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
from bitstampex.api import API

# Import Homebrew

log = logging.getLogger(__name__)

class Client:
    def __init__(self, server_addr, key=None):
        self.__server_addr = server_addr
        self.__key = key

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.sendto(json.dumps(message).encode('ascii'), self.__server_addr)
        print(message)

    def listen(self, endpoint, q={}, private=False):
        api = API()

        while True:
            print("listening!")
            if private:
                api.load_key(self.__key)
                resp = api.query_private(endpoint, q)
            else:
                resp = api.query_public(endpoint, q)
            self.format_orderbook('BTCUSD', resp)
            time.sleep(5)

    def format_orderbook(self, symbol, js):
        print(js)
        ts = js['timestamp']

        asks = js['asks'][0]
        ask_p = asks[0]
        ask_v = asks[1]

        bids = js['bids'][0]
        bid_p = bids[0]
        bid_v = bids[1]

        msg = '\t'.join([ts, symbol,'bitstamp', 'Ask Vol', ask_v])
        self.send(msg)
        msg = '\t'.join([ts, symbol,'bitstamp', 'Ask Price', ask_p])
        self.send(msg)
        msg = '\t'.join([ts, symbol, 'bitstamp', 'Bid Vol', bid_v])
        self.send(msg)
        msg = '\t'.join([ts, symbol, 'bitstamp', 'Bid Price', bid_p])
        self.send(msg)
        return

if __name__ == '__main__':
    uix = Client(('localhost', 6666), key='./bitstamp.key')
    uix.listen('order_book/btcusd/', private=False)