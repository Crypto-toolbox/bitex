"""
http://docs.bitfinex.com/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BitfinexREST
from bitex.utils import return_json
from bitex.formatters.bitfinex import trade, cancel, order_status
# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitfinex(BitfinexREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bitfinex, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """
    @return_json(None)
    def order_book(self, pair, **kwargs):
        return self.public_query('book/%s' % pair, params=kwargs)

    @return_json(None)
    def ticker(self, pair, **kwargs):
        return self.public_query('pubticker/%s' % pair, params=kwargs)

    @return_json(None)
    def trades(self, pair, **kwargs):
        return self.public_query('trades/%s' % pair, params=kwargs)

    def _place_order(self, pair, amount, price, side, replace, **kwargs):
        q = {'symbol': pair, 'amount': amount, 'price': price, 'side': side,
             'type': 'exchange limit'}
        q.update(kwargs)
        if replace:
            return self.private_query('order/cancel/replace', params=q)
        else:
            return self.private_query('order/new', params=q)

    @return_json(trade)
    def bid(self, pair, price, amount, replace=False, **kwargs):
        return self._place_order(pair, amount, price, 'buy', replace=replace,
                                 **kwargs)

    @return_json(trade)
    def ask(self, pair, price, amount, replace=False, **kwargs):
        return self._place_order(pair, str(amount), str(price), 'sell',
                                 replace=replace, **kwargs)

    @return_json(cancel)
    def cancel_order(self, order_id, all=False, **kwargs):

        q = {'order_id': int(order_id)}
        q.update(kwargs)
        if not all:
            return self.private_query('order/cancel', params=q)
        else:
            endpoint = 'order/cancel/all'
            return self.private_query(endpoint)

    @return_json(order_status)
    def order(self, order_id, **kwargs):
        q = {'order_id': order_id}
        q.update(kwargs)
        return self.private_query('order/status', params=q)

    @return_json(None)
    def balance(self, **kwargs):
        return self.private_query('balances', params=kwargs)

    @return_json(None)
    def withdraw(self, _type, source_wallet, amount, tar_addr, **kwargs):
        q = {'withdraw_type': _type, 'walletselected': source_wallet,
             'amount': amount, 'address': tar_addr}
        q.update(kwargs)
        return self.private_query('withdraw', params=q)

    @return_json(None)
    def deposit_address(self, **kwargs):
        q = {'method': currency, 'wallet_name': target_wallet}
        q.update(kwargs)
        return self.private_query('deposit/new', params=kwargs)

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def statistics(self, pair):
        return self.public_query('stats/%s' % pair)

    @return_json(None)
    def funding_book(self, currency, **kwargs):
        return self.public_query('lendbook/%s' % currency, params=kwargs)

    @return_json(None)
    def lends(self, currency, **kwargs):
        return self.public_query('lends/%s' % currency, params=kwargs)

    @return_json(None)
    def pairs(self, details=False):
        if details:
            return self.public_query('symbols_details')
        else:
            return self.public_query('symbols')

    @return_json(None)
    def fees(self):
        return self.private_query('account_infos')

    @return_json(None)
    def orders(self):
        return self.private_query('orders')

    @return_json(None)
    def balance_history(self, currency, **kwargs):
        q = {'currency': currency}
        q.update(kwargs)
        return self.private_query('history/movements', params=q)

    @return_json(None)
    def trade_history(self, pair, since, **kwargs):
        q = {'symbol': pair, 'timestamp': since}
        q.update(kwargs)
        return self.private_query('mytrades', params=q)


