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
    def __init__(self, server_addr, pair, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitfinexHTTP, self).__init__(server_addr, api, 'Bitfinex', pair)

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(BitfinexHTTP, self).send(messasge)

    def format_orderbook(self, js):
        asks = js['asks'][0]
        ask_p = asks['price']
        ask_v = asks['amount']
        ask_ts = asks['timestamp']
        bids = js['bids'][0]
        bid_p = bids['price']
        bid_v = bids['amount']
        bid_ts = bids['timestamp']
        formatted = [[ask_ts, 'Ask Vol', ask_v],
                     [ask_ts, 'Ask Price', ask_p],
                     [bid_ts, 'Bid Vol', bid_v],
                     [bid_ts, 'Bid Price', bid_p]]
        return formatted

    def query_ob(self, limit_orders=50, aggregrate=True):
        q = {'limit_asks': limit_orders, 'limit_bids': limit_orders}
        if not aggregrate:
            q['group'] = 0

        sent = time.time()
        resp = self._query()









if __name__ == '__main__':
    uix = Client(('localhost', 6666), './bitfinex.key')
    uix.listen('book/BTCUSD', private=False)