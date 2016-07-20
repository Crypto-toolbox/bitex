"""
Task:
Supplies an REST API Interface to the specified exchange.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.rest import BitstampREST
from bitex.http.client import Client
log = logging.getLogger(__name__)


class BitstampHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = BitstampREST(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BitstampHTTP, self).__init__(api, 'Bitstamp')

    def order_book(self, pair, count=0):
        q = {'pair': pair}
        if count:
            q['count'] = count

        resp = self.query('v2/order_book/%s/' % pair)

        return resp

    def ticker(self, pair):
        response = self.query('v2/ticker/%s/' % pair)
        return response

    def hourly_ticker(self, pair):
        resp = self.query('v2/ticker_hour/%s/' % pair)
        return resp

    def trades(self, pair, t='hour'):
        resp = self.query('v2/transactions/%s/' % pair, data={'time': t})
        return resp

    def eur_usd_conversion(self):
        return self.query('v2/eur_usd/')

    def balance(self, pair=''):
        if pair:
            return self.query('v2/balance/%s/' % pair, authenticate=True,
                              req_type='POST', data={})
        else:
            return self.query('balance/', authenticate=True, req_type='POST',
                              data={})

    def user_transactions(self, pair='', offset=0, limit=100, sort='desc'):
        q = {'offset': offset, 'limit': limit, 'sort': sort}
        if pair:
            return self.query('v2/user_transactions/%s/' % pair, data=q,
                               req_type='POST', authenticate=True)
        else:
            return self.query('v2/user_transactions/', data=q,
                               req_type='POST', authenticate=True)

    def open_orders(self, pair):
        return self.query('v2/open_orders/%s/' % pair, req_type='POST',
                          authenticate=True)

    def order_status(self, id):
        return self.query('order_status/', data={'id': id}, req_type='POST',
                          authenticate=True)

    def cancel_order(self, id=None):
        if id is None:
            return self.query('cancel_all_orders/', req_type='POST',
                              authenticate=True)
        else:
            return self.query('v2/cancel_order/', data={'id': id},
                              req_type='POST', authenticate=True)

    def limit_order(self, order_type, pair, amount, price, limit_price=None):
        if order_type != 'sell' and order_type != 'buy':
            raise ValueError(' order_type argument must be equal to "sell" or "buy"')

        q = {'amount': amount, 'price': price}
        if limit_price is not None:
            q['limit_price'] = limit_price
        return self.query('v2/%s/%s/' % (order_type, pair), data=q,
                          req_type='POST', authenticate=True)

    def withdrawal_requests(self):
        return self.query('withdrawal_requests/', req_type='POST',
                          authenticate=True)

    def bitcoin_withdrawal(self, address, amount, instant=0):
        q = {'address': address, 'amount': amount, 'instant': instant}
        return self.query('bitcoin_withdrawal/', data=q, req_type='POST',
                          authenticate=True)

    def bitcoin_address(self):
        return self.query('bitcoin_deposit_address/', req_type='POST',
                          authenticate=True)

    def unconfirmed_bitcoin_deposits(self):
        return self.query('unconfirmed_bts/', req_type='POST', authenticate=True)

    def ripple_withdrawal(self, address, amount, currency):
        q = {'address': address, 'amount': amount, 'currency': currency}
        return self.query('ripple_withdrawal/', data=q, req_type='POST',
                          authenticate=True)

    def ripple_address(self):
        return self.query('ripple_address/', req_type='POST', authenticate=True)

    def transfer_to_main(self, currency, amount, to_sub=None):
        q = {'currency': currency, 'amount': amount}
        if to_sub:
            q['subAccount'] = to_sub
        return self.query('v2/transfer-to-main', data=q, req_type='POST',
                          authenticate=True)

    def transfer_to_sub(self, currency, amount, sub_account):
        q = {'currency': currency, 'amount': amount, 'subAccount': sub_account}
        return self.query('v2/transfer-from-main', data=q, req_type='POST',
                          authenticate=True)


if __name__ == '__main__':
    uix = BitstampHTTP()
    print(uix.ticker('btcusd').text)
    print(uix.balance('btcusd').text)

