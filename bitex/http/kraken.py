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
from ..api.kraken import API

# Import Homebrew

log = logging.getLogger(__name__)

class Client:
    def __init__(self, server_addr, key=None):
        self.__server_addr = server_addr
        self.__key = key

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.sendto(json.dumps(message).encode('ascii'),
        #                   self.__server_addr)
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
            self.send(resp)
            time.sleep(5)

if __name__ == '__main__':
    uix = Client(('localhost', 6666), './kraken.key')
    uix.listen('Balance', q={'asset':'ZEUR'}, private=True)
