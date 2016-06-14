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

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(KrakenHTTP, self).send(message)

    def format_ob(self, input):
        ask_p, ask_v, ask_t = input['result'][self._pair]['asks'][0]
        bid_p, bid_v, bid_t = input['result'][self._pair]['bids'][0]
        formatted = [[ask_t, 'Ask Price', ask_p],
                     [ask_t, 'Ask Vol', ask_v],
                     [bid_t, 'Bid Price',  bid_p],
                     [bid_t, 'Bid Vol', bid_v]]
        return formatted

    def query_ob(self, count=0):
        q = {'pair': self._pair}
        if count:
            q['count'] = count

        sent = time.time()
        resp = self._query('Depth', q)
        received = time.time()
        formatted = self.format_ob(resp)
        for i in formatted:
            self.send(super(KrakenHTTP, self)._format(sent, received, *i))


if __name__ == '__main__':
    test = KrakenHTTP(('localhost', 676), 'XXBTZEUR')
    test.query_ob()
