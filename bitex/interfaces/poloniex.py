"""
http://docs.bitfinex.com/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import PoloniexREST
from bitex.utils import return_json
from bitex.formatters.poloniex import trade, cancel
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

    """
    BitEx Standardized Methods
    """

    @return_json(None)
    def ticker(self, pair, **kwargs):
        return self.public_query('returnTicker', params=kwargs)

    @return_json(None)
    def order_book(self, pair, **kwargs):
        kwargs['currencyPair'] = pair
        return self.public_query('returnOrderBook', params=kwargs)

    @return_json(None)
    def trades(self, pair, **kwargs):
        kwargs['currencyPair'] = pair
        return self.public_query('returnTradeHistory', params=kwargs)

    @return_json(trade)
    def bid(self, pair, rate, amount, **kwargs):
        q = {'command': 'buy', 'currencyPair': pair, 'amount': amount,
             'rate': rate}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(trade)
    def ask(self, pair, rate, amount, **kwargs):
        q = {'command': 'sell', 'currencyPair': pair, 'amount': amount,
             'rate':    rate}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(cancel)
    def cancel_order(self, txid, **kwargs):
        q = {'orderNumber': txid, 'command': 'cancelOrder'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(None)
    def balance(self, detailed=False, **kwargs):
        if detailed:
            q['command'] = 'returnCompleteBalances'
            return self.private_query('tradingApi', params=kwargs)
        else:
            q['command'] = 'returnBalances'
            return self.private_query('tradingApi', params=kwargs)

    @return_json(None)
    def withdraw(self, amount, tar_addr, **kwargs):
        q = {'currency': kwargs.pop('currency'), 'amount': amount, 'address': tar_addr}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(None)
    def deposit_address(self, currency, **kwargs):
        q = {'command': 'returnDepositAddresses'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)


    """
    Exchange Specific Methods
    """

    @return_json(None)
    def currencies(self):
        return self.public_query('returnCurrencies')

    @return_json(None)
    def hloc(self, pair, **kwargs):
        kwargs['currencyPair'] = pair
        return self.public_query('returnChartData')


    @return_json(None)
    def balance_history(self, **kwargs):
        q = {'command': 'returnDepositsWithdrawals'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(None)
    def orders(self, pair='all', **kwargs):
        q = {'command': 'returnOpenOrders', 'currencyPair': pair}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(None)
    def trade_history(self, pair='all', **kwargs):
        q = {'currencyPair': pair, 'command': 'returnTradeHistory'}
        q.update(kwargs)
        return self.private_query('tradingApi', params=q)

    @return_json(None)
    def update_order(self, txid, rate, **kwargs):
        q = {'command': 'moveOrder', 'rate': rate, 'orderNumber': txid}
        q.update(kwargs)
        return self.query('tradingApi', params=q)

    @return_json(None)
    def fees(self):
        return self.private_query('tradingApi',
                                  params={'command': 'returnFeeInfo'})
