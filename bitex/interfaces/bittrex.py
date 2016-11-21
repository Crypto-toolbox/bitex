"""
https://bittrex.com/Home/Api
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BittrexREST
from bitex.utils import return_json
from bitex.formatters.bittrex import trade, cancel, order_book
# Init Logging Facilities
log = logging.getLogger(__name__)


class Bittrex(BittrexREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bittrex, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', 'public/' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)

    @return_json(None)
    def pairs(self):
        return self.public_query('getmarkets')

    @return_json(None)
    def currencies(self):
        return self.public_query('getcurrencies')

    @return_json(None)
    def ticker(self, pair):
        return self.public_query('getticker', params={'market': pair})

    @return_json(None)
    def statistics(self, pair=None):
        if pair:
            return self.public_query('getmarketsummary', params={'market': pair})
        else:
            return self.public_query('getmarketsummaries')

    @return_json(order_book)
    def order_book(self, pair, side='both', **kwargs):
        q = {'market': pair, 'type': side}
        q.update(kwargs)
        return self.public_query('getorderbook', params=q)

    @return_json(None)
    def trades(self, pair, **kwargs):
        q = {'market': pair}
        q.update(kwargs)
        return self.public_query('getmarkethistory', params=q)

    @return_json(trade)
    def bid(self, pair, price, vol, market=False, **kwargs):
        q = {'market': pair, 'rate': price, 'quantity': vol}
        q.update(kwargs)
        if market:
            # send market order
            return self.private_query('market/buymarket', params=q)
        else:
            # send limit order
            return self.private_query('market/buylimit', params=q)

    @return_json(trade)
    def ask(self, pair, price, vol, market=False, **kwargs):
        q = {'market': pair, 'rate': price, 'quantity': vol}
        q.update(kwargs)
        if market:
            # send market order
            return self.private_query('market/sellmarket', params=q)
        else:
            # send limit order
            return self.private_query('market/selllimit', params=q)

    @return_json(None)
    def balance(self):
        return self.private_query('account/getbalances')

    @return_json(cancel)
    def cancel_order(self, txid):
        q = {'uuid': txid}
        return self.private_query('market/cancel', params=q)
