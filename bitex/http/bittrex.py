"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.bittrex import API
from bitex.http.client import Client

log = logging.getLogger(__name__)


class BittrexHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(BittrexHTTP, self).__init__(api, 'Bitstamp')

    def markets(self):
        return self.query('public/getmarkets')

    def ticker(self, pair):
        response = self.query('public/getticker', params={'market': pair})
        return response

    def currencies(self):
        return self.query('public/getcurrencies')

    def market_summaries(self, pair=None):
        if pair is None:
            return self.query('public/getmarketsummaries')
        else:
            return self.query('public/getmarketsummary', params={'market': pair})

    def order_book(self, pair, order_type='both', depth=20):
        return self.query('public/getorderbook', params={'market': pair,
                                                         'type': order_type,
                                                         'depth': depth})

    def trades(self, pair, count=20):
        return self.query('public/getmarkethistory', params={'market': pair,
                                                             'count': count})

    def add_order(self, price, vol, pair, side, order_type='limit'):
        """
        Places an order.
        :param price:
        :param vol:
        :param pair:
        :param side: bid or ask
        :param order_type: market or limit
        :return:
        """
        q = {'market': pair, 'quantity': vol, 'rate': price}
        if side == 'bid':
            self.query('market/buy%s' % order_type, params=q, authenticate=True)
        elif side == 'ask':
            self.query('market/sell%s' % order_type, params=q, authenticate=True)
        else:
            raise ValueError("'side' arg must be 'bid' or 'ask'!")

    def cancel_order(self, uuid):
        self.query('market/cancel', params={'uuid': uuid}, authenticate=True)

    def orders(self, pair):
        return self.query('market/getopenorders', params={'market': pair},
                          authenticate=True)

    def order(self, uuid):
        return self.query('account/getorder', params={'uuid': uuid},
                          authenticate=True)

    def balance(self, currency=None):
        if currency is None:
            return self.query('account/getbalances', authenticate=True)
        else:
            return self.query('account/getbalance', params={'currency': currency},
                              authenticate=True)

    def deposit_address(self, currency):
        return self.query('account/getdepositaddress', params={'currency': currency},
                          authenticate=True)

    def withdraw(self, currency, vol, to_address, payment_id=None):
        q = {'currency': currency, 'quantity': vol, 'address': to_address}
        if payment_id:
            q['paymentid'] = payment_id

        return self.query('account/withdraw', params=q, authenticate=True)

    def ledger(self, pair, count=20):
        """
        Return history of orders.
        :param pair:
        :param count:
        :return:
        """
        q = {'market': pair, 'count': count}
        return self.query('account/getorderhistory', params=q,
                          authenticate=True)

    def funding_history(self, history_type, currency, count=20):
        q = {'currency': currency, 'count': count}
        if history_type == 'deposit' or history_type == 'withdrawal':
            return self.query('acount/get%shistory', params=q, authenticate=True)
        else:
            raise ValueError("History type must be 'deposit' or 'withdrawal'!")


if __name__ == '__main__':
    uix = BittrexHTTP(key='a64db1b5779246fb9dd907ab9571acff', secret='c5011fe2731f40ccb52fa32ab76251ba')
    print(uix._api.key, uix._api.secret)
    print(uix.markets().json())
    print(uix.ledger('BTC-LTC').text)

