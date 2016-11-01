"""
http://docs.bitfinex.com/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import PoloniexREST
from bitex.utils import return_json
# Init Logging Facilities
log = logging.getLogger(__name__)


class Poloniex(PoloniexREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Poloniex, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', 'public?command=' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint,
                          authenticate=True, **kwargs)

    @return_json
    def ticker(self):
        return self.public_query('returnTicker')

    @return_json
    def order_book(self, pair, **kwargs):
        kwargs['currencyPair'] = pair
        return self.public_query('returnOrderBook', params=kwargs)

    @return_json
    def trades(self, pair, **kwargs):
        kwargs['currencyPair'] = pair
        return self.public_query('returnTradeHistory', params=kwargs)

    @return_json
    def currencies(self):
        return self.public_query('returnCurrencies')

    @return_json
    def hloc(self, pair, **kwargs):
        kwargs['currencyPair'] = pair
        return self.public_query('returnChartData')

    @return_json
    def balance(self, detailed=False):
        q = {}
        if detailed:
            q['command'] = 'returnCompleteBalances'
            return self.private_query('tradingApi', params=q)
        else:
            q['command'] = 'returnBalances'
            return self.private_query('tradingApi', params=q)

    @return_json
    def addresses(self):
        q = {'command': 'returnDepositAddresses'}
        return self.private_query('tradingApi', params=q)

    @return_json
    def balance_history(self, **kwargs):
        q = {'command': 'returnDepositsWithdrawals'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json
    def orders(self, pair='all', **kwargs):
        q = {'command': 'returnOpenOrders', 'currencyPair': pair}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json
    def trade_history(self, pair='all', **kwargs):
        q = {'currencyPair': pair, 'command': 'returnTradeHistory'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json
    def bid(self, pair, amount, rate, **kwargs):
        q = {'command': 'buy', 'currencyPair': pair, 'amount': amount,
             'rate': rate}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)


    @return_json
    def ask(self, pair, rate, amount, **kwargs):
        q = {'command': 'buy', 'currencyPair': pair, 'amount': amount,
             'rate':    rate}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json
    def cancel_order(self, txid, **kwargs):
        q = {'orderNumber': txid, 'command': 'cancelOrder'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json
    def update_order(self, txid, rate, **kwargs):
        q = {'command': 'moveOrder', 'rate': rate, 'orderNumber': txid}
        q.update(kwargs)
        return self.query('tradingApi', params=q)


