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
try:
    from ..api.kraken import API
except SystemError:
    from bitex.api.kraken import API
from bitex.http.client import Client

log = logging.getLogger(__name__)


class KrakenHTTP(Client):
    def __init__(self, server_addr, pair, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(KrakenHTTP, self).__init__(server_addr, api, 'Kraken', pair)

    def format_ob(self, sent, received, input):
        ask_p, ask_v, ask_t = input['result'][self._pair]['asks'][0]
        bid_p, bid_v, bid_t = input['result'][self._pair]['bids'][0]
        formatted = [['ask', ask_t, ask_p, ask_v],
                     ['bid', bid_t, bid_p, bid_v]]

        for i in formatted:
            self.send(super(KrakenHTTP, self)._format(sent, received, *i))

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.sendto(json.dumps(message).encode('ascii'),
        #                   self.__server_addr)
        print(message)

    def listen_ob(self, count=0):
        q = {'pair': self._pair}
        if count:
            q['count'] = count

        while True:
            print("listening!")
            sent = time.time()
            resp = self._listen('Depth', q)
            received = time.time()
            self.format_ob(sent, received, resp)
            time.sleep(5)

if __name__ == '__main__':
    test = KrakenHTTP(('localhost', 67676), 'XXBTZEUR')
    test.listen_ob()
