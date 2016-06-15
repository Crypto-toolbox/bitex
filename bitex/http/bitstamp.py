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

    def ticker(self, pair):
        return self._query('ticker/%s/' % pair, q)

    def hourly_ticker(self, pair):
        return self._query('ticker_hour/%s/' % pair, q)

    def trades(self, pair, t='hour'):
        return self._query('transactions/%s/' % pair, {'time': t})

    def eur_usd_conversion(self):
        return self._query('eur_usd/')

    def balance(self, pair=''):
        if pair:
            return self._query('balance/%s/' % pair, private=True)
        else:
            return self,_api._query('balance/', private=True)

    def user_transactions(self, pair='', offset=0, limit=100, sort='desc'):
        q = {'offset': offset, 'limit': limit, 'sort': sort}
        if pair:
            return self._query('user_transactions/%s/' % pair, q,
                                    private=True)
        else:
            return self, _api._query('user_transactions/', q, private=True)

    def open_orders(self, pair):
        return self._query('v2/open_orders/%s/' % pair, private=True)

    def order_status(self, id):
        return self._query('v2/order_status/', {'id': id}, private=True)

    def cancel_order(self, id, all=False, api='api'):
        if all:
            return self._query('/cancel_all_orders/', private=True)
        else:
            return self._query('/cancel_order/', {'id': id}, private=True)

    def limit_order(self, order_type, pair, amount, price, limit_price=None):
        if order_type != 'sell' and order_type != 'buy':
            raise ValueError(' order_type argument must be equal to "sell" or "buy"')

        q = {'amount': amount, 'price': price}
        if limit_price is not None:
            q['limit_price'] = limit_price
        return self._query('v2/%s/%s/' % (order_type, pair), q, private=True)

    def withdrawal_requests(self):
        return self._query('/withdrawal_requests/', private=True)

    def bitcoin_withdrawal(self, address, amount, instant=0):
        q = {'address': address, 'amount': amount, 'instant': instant}
        return self._query('bitcoin_withdrawal/', q, private=True)

    def bitcoin_address(self):
        return self._query('bitcoin_deposit_address/', private=True)

    def unconfirmed_bitcoin_deposits(self):
        return self._query('unconfirmed_bts/', private=True)

    def ripple_withdrawal(self, address, amount):
        q = {'address': address, 'amount': amount}
        pass  # See https://github.com/nlsdfnbch/bitex/issues/4

    def ripple_address(self):
        return self._query('')

    def transfer_to_main(self, currency, amount, to_sub=None):
        q = {'currency': currency, 'amount': amount}
        if to_sub:
            q['subAccount'] = to_sub
        return self._query('v2/transfer-to-main', q, private=True)

    def transfer_to_sub(self, currency, amount, sub_account):
        q = {'currency': currency, 'amount': amount, 'subAccount': sub_account}
        return self._query('v2/transfer-to-main', q , private=True)


if __name__ == '__main__':
    uix = BitstampHTTP(('localhost', 676), key_file='../../keys/bitstamp.key')
    print(uix.withdrawal_requests())
