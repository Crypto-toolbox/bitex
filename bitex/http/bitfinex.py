"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.bitfinex import API
from bitex.http.client import Client


log = logging.getLogger(__name__)


class BitfinexHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitfinexHTTP, self).__init__(api, 'Bitfinex')

    def order_book(self, pair, limit_orders=50, aggregrate=True):
        q = {'limit_asks': limit_orders, 'limit_bids': limit_orders}
        if not aggregrate:
            q['group'] = 0
        return self.query('/book/%s/' % pair, q)

    def funding_book(self, pair, limit_bids=50, limit_asks=50):
        q = {'limit_bids': limit_bids, 'limit_asks': limit_asks}
        return self.query('lendbook/%s/' % pair, params=q)

    def ticker(self, pair):
        return self.query("pubticker/%s" % pair)

    def stats(self, pair):
        return self.query("stats/%s" % pair)

    def trades(self, pair, start_time=None, limit_trades=False):
        q = {'limit_trades': limit_trades}
        if start_time:
            q['timestamp'] = start_time
        return self.query('trades/%s' % pair, params=q)

    def lends(self, pair, start_time=None, limit_lends=False):
        q = {'limit_lends': limit_lends}
        if start_time:
            q['timestamp'] = start_time
        return self.query('lends/%s' % pair, params=q)

    def pairs(self, verbose=False):
        if verbose:
            return self.query('symbols_details')
        else:
            return self.query('symbols')

    def account_infos(self):
        return self.query('account_infos', authenticate=True, post=True)

    def summary(self):
        return self.query('summary', authenticate=True, post=True)

    def deposit_crypto(self, coin, wallet_name, renew=False):
        q = {'method': coin, 'wallet_name': wallet_name}
        if renew:
            q['renew'] = 1
        return self.query('deposit/new', params=q, authenticate=True, post=True)

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

        return self.query('order/new', params=q, authenticate=True, post=True)

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
            return self.query('order/cancel/multi', params=q, authenticate=True,
                              post=True)
        else:
            return self.query('order/cancel', params=q, authenticate=True,
                              post=True)

    def cancel_all_orders(self):
        return self.query('order/cancel/all', authenticate=True, post=True)

    def replace_order(self, order_id, pair, amount, price, side,
                      exchange='bitfinex', order_type='limit', hidden=False,
                      use_remaining_amount=False):
        q = {'order_id': order_id, 'symbol': pair, 'amount': amount,
             'price': price, 'side': side, 'exchange': exchange,
             'is_hidden': hidden, 'use_remaining': use_remaining_amount}

        return self.query('order/cancel/replace', params=q, authenticate=True,
                          post=True)

    def order_status(self, order_id):
        q = {'order_id': order_id}
        return self.query('order/status', params=q, authenticate=True,
                          post=True)

    def orders(self):
        return self.query('order/status', authenticate=True, post=True)

    def positions(self):
        return self.query('positions', authenticate=True, post=True)

    def claim_position(self,position_id, amount):
        q = {'position_id': position_id, 'amount': amount}
        return self.query('position/claim', params=q, authenticate=True,
                          post=True)

    def balance_history(self, currency, since=None, until=None, limit=500,
                        wallet=None):
        q = {'currency': currency, 'limit': limit}
        if since:
            q['since'] = since

        if until:
            q['until'] = until

        if wallet:
            q['wallet'] = wallet

        return self.query('history', params=q, authenticate=True, post=True)

    def funding_history(self, currency, method=None, since=None, until=None,
                        limit=500):
        q = {'currency': currency, 'limit': limit}
        if method:
            q['method'] = method

        if since:
            q['since'] = since

        if until:
            q['until'] = until

        return self.query('history/movements', params=q, authenticate=True,
                          post=True)

    def trade_history(self, pair, timestamp=None, until=None,
                        limit_trades=50, reverse=False):
        q = {'symbol': pair, 'limit_trades': limit_trades}
        if reverse:
            q['reverse'] = 1

        if timestamp:
            q['timestamp'] = timestamp

        if until:
            q['until'] = until

        return self.query('mytrades', params=q, authenticate=True, post=True)

    def balance(self):
        return self.query('balances', authenticate=True, post=True)

    def margin_information(self):
        return self.query('margin_infos', authenticate=True, post=True)

    def transfer(self, currency, amount, from_, to_):
        q = {'currency': currency, 'amount': amount, 'walletfrom': from_,
             'walletto': to_}
        return self.query('transfer', params=q, authenticate=True, post=True)

    def withdraw_crypto(self, coin_type, wallet, amount, address):
        q = {'withdraw_type':  coin_type, 'walletselected': wallet,
             'amount':         amount, 'address': address}

        return self.query('withdraw', params=q, authenticate=True, post=True)

    def withdraw_fiat(self, from_wallet, amount, account_name, account_number,
                      bank_name, bank_addr, bank_city, bank_country,
                      express_wire=False, **intermediary_kwargs):
        q = {'withdraw_type':  'wire', 'walletselected': from_wallet,
             'amount':         amount, 'account_name': account_name,
             'account_number': account_number, 'bank_name': bank_name,
             'bank_address':   bank_addr, 'bank_city': bank_city,
             'bank_country':   bank_country}

        if express_wire:
            q['expressWire'] = 1

        for kwarg in intermediary_kwargs:
            q[kwarg] = intermediary_kwargs[kwarg]

        return self.query('withdraw', params=q, authenticate=True, post=True)

    def key_permissions(self):
        return self.query('key_infos', authenticate=True, post=True)

if __name__ == '__main__':
    uix = BitfinexHTTP()
    print(uix.ticker('ltcbtc').text)
