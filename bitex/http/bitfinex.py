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
    def __init__(self, server_addr, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitfinexHTTP, self).__init__(server_addr, api, 'Bitfinex')

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(message).encode('ascii'), self._receiver)
        super(BitfinexHTTP, self).send(message)

    def order_book(self, pair, limit_orders=50, aggregrate=True):
        q = {'limit_asks': limit_orders, 'limit_bids': limit_orders}
        if not aggregrate:
            q['group'] = 0
        return self._query('/book/%s/' % pair, q)

    def funding_book(self, pair, limit_bids=50, limit_asks=50):
        q = {'limit_bids': limit_bids, 'limit_asks': limit_asks}
        return self._query('/lendbook/%s/' % pair, q)

    def ticker(self, pair):
        return self._query("/pubticker/%s/" % pair)

    def stats(self, pair):
        return self._query("/stats/%s/" % pair)

    def trades(self, pair, start_time=None, limit_trades=False):
        q = {'limit_trades': limit_trades}
        if start_time:
            q['timestamp'] = start_time
        return self._query('/trades/%s' % pair, q)

    def lends(self, pair, start_time=None, limit_lends=False):
        q = {'limit_lends': limit_lends}
        if start_time:
            q['timestamp'] = start_time
        return self._query('/lends/%s' % pair, q)

    def pairs(self, verbose=False):
        if verbose:
            return self._query('/symbols_details/')
        else:
            return self._query('/symbols/')

    def account_infos(self):
        return self._query('/account_infos/', private=True)

    def summary(self):
        return self._query('/summary', private=True)

    def deposit_crypto(self, coin, wallet_name, renew=False):
        q = {'method': coin, 'wallet_name': wallet_name}
        if renew:
            q['renew'] = 1
        return self._query('/deposit/new/', q, private=True)

    def _add_order(self, trade, pair, amount, price, post_only=False,
                   hide=False, ocoorder=None):
        q = {'side': trade, 'symbol': pair, 'price': price, 'amount': amount,
             'exchange': 'bitfinex'}
        if hide:
            q['hide'] = True

        if post_only:
            q['is_postonly'] = True

        if ocoorder:
            q['ocoorder'] = True
            q['buy_price_oco'] = ocoorder

        return self._query('/order/new/', q, private=True)

    def add_buy_order(self, pair, amount, price, post_only=False, hide=False,
                      ocoorder=None):
        return self._add_order('buy', pair, amount, price, post_only, hide,
                               ocoorder)

    def add_sell_order(self, pair, amount, price, post_only=False, hide=False,
                  ocoorder=None):
            return self._add_order('sell', pair, amount, price, post_only, hide,
                                   ocoorder)

    def cancel_order(self, *order_id):
        q = {'order_id': order_id}
        if isinstance(order_id, (list, tuple)):
            return self._query('/order/cancel/multi', q, private=True)
        else:
            return self._query('/order/cancel/', q, private=True)

    def cancel_all_orders(self):
        return self._query('/order/cancel/all', private=True)

    def replace_order(self, order_id, pair, amount, price, side,
                      exchange='bitfinex', order_type='limit', hidden=False,
                      use_remaining_amount=False):
        q = {'order_id': order_id, 'symbol': pair, 'amount': amount,
             'price': price, 'side': side, 'exchange': exchange,
             'is_hidden': hidden, 'use_remaining': use_remaining_amount}

        return self._query('/order/cancel/replace', q, private=True)

    def order_status(self, order_id):
        q = {'order_id': order_id}
        return self._query('/order/status/', q, private=True)

    def orders(self):
        return self._query('/order/status/', private=True)

    def positions(self):
        return self._query('/positions/', private=True)

    def claim_position(self,position_id, amount):
        q = {'position_id': position_id, 'amount': amount}
        return self._query('/position/claim/', q, private=True)

    def balance_history(self, currency, since=None, until=None, limit=500,
                        wallet=None):
        q = {'currency': currency, 'limit': limit}
        if since:
            q['since'] = since

        if until:
            q['until'] = until

        if wallet:
            q['wallet'] = wallet

        return self._query('/history/', q, private=True)

    def funding_history(self, currency, method=None, since=None, until=None,
                        limit=500):
        q = {'currency': currency, 'limit': limit}
        if method:
            q['method'] = method

        if since:
            q['since'] = since

        if until
            q['until'] = until

        return self._query('/history/movements/', q, private=True)

    def trade_history(self, pair, timestamp=None, until=None,
                        limit_trades=50, reverse=False):
        q = {'symbol': pair, 'limit_trades': limit_trades}
        if reverse:
            q['reverse'] = 1

        if timestamp:
            q['timestamp'] = timestamp

        if until:
            q['until'] = until

        return self._query('/mytrades/', q, private=True)




if __name__ == '__main__':
    uix = BitfinexHTTP(('localhost', 6666), 'BTCUSD')
    uix.orderbook('BTCUSD')