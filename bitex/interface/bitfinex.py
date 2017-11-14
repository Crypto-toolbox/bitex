"""Bitfinex Interface class."""
# Import Built-Ins
import logging

# Import Third-Party
import requests

# Import Homebrew
from bitex.api.REST.bitfinex import BitfinexREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_version_compatibility, check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitfinex(RESTInterface):
    """Bitfinex Interface class.

    Includes standardized methods, as well as all other Endpoints
    available on their REST API.
    """
    # pylint: disable=arguments-differ

    # State version specific methods
    v2_only_methods = ['candles', 'market_average_price', 'wallets', 'orders',
                       'order_trades', 'positions', 'offers', 'funding_info',
                       'performance', 'alert_set', 'alert_list',
                       'alert_delete', 'calc_available_balance']
    v1_only_methods = ['new_order', 'tickers', 'symbols', 'symbols_details',
                       'account_info', 'account_fees', 'summary', 'deposit',
                       'key_info', 'balances', 'transfer', 'withdrawal',
                       'cancel_order', 'order_status', 'open_orders',
                       'cancel_all_orders', 'cancel_multiple_orders',
                       'replace_order', 'active_orders', 'active_positions',
                       'active_credits', 'balance_history', 'past_trades',
                       'deposit_withdrawal_history', 'new_offer', 'cancel_offer',
                       'offer_status', 'unused_taken_funds', 'taken_funds',
                       'total_taken_funds', 'close_funding', 'basket_manage',
                       'lends', 'funding_book']

    def __init__(self, **api_kwargs):
        super(Bitfinex, self).__init__('Bitfinex', BitfinexREST(**api_kwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if not authenticate:
            return super(Bitfinex, self).request('GET', endpoint, authenticate=authenticate,
                                                 **req_kwargs)
        return super(Bitfinex, self).request('POST', endpoint, authenticate=authenticate,
                                             **req_kwargs)

    def _get_supported_pairs(self):
        if self.REST.version == 'v1':
            return self.symbols().json()
        return requests.get('https://api.bitfinex.com/v1/symbols').json()

    ###############
    # Basic Methods
    ###############
    @check_and_format_pair
    def ticker(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('pubticker/%s' % pair)
        return self.request('ticker/%s' % pair, params=endpoint_kwargs)

    @check_and_format_pair
    def order_book(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('book/%s' % pair, params=endpoint_kwargs)
        prec = ('P0' if 'Precision' not in endpoint_kwargs else
                endpoint_kwargs.pop('Precision'))
        return self.request('book/%s/%s' % (pair, prec),
                            params=endpoint_kwargs)

    @check_and_format_pair
    def trades(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('trades/%s' % pair, params=endpoint_kwargs)
        return self.request('trades/%s/hist' % pair, params=endpoint_kwargs)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy', **kwargs)

    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'symbol': pair, 'price': price, 'amount': size, 'side': side,
                   'type': 'exchange-limit'}
        payload.update(kwargs)
        return self.new_order(pair, **payload)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def order_status(self, order_id, *args, **kwargs):
        return self.request('order/status', authenticate=True, params={'order_id': order_id})

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def open_orders(self, *args, **kwargs):
        return self.active_orders(*args, **kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'order_id': oid})
            r = self.request('order/cancel', authenticate=True,
                             params=payload)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.balances()

    ###########################
    # Exchange Specific Methods
    ###########################

    #########################
    # Version Neutral Methods
    #########################

    @check_and_format_pair
    def stats(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('stats/%s' % pair)
        key = endpoint_kwargs.pop('key')
        size = endpoint_kwargs.pop('size')
        side = endpoint_kwargs.pop('side')
        section = endpoint_kwargs.pop('section')
        path = key, size, pair, side, section
        return self.request('stats1/%s:%s:%s:%s/%s' % path, params=endpoint_kwargs)

    def margin_info(self, **endpoint_kwargs):
        if self.REST.version == 'v1':
            return self.request('margin_info', authenticate=True)
        key = endpoint_kwargs.pop('key')
        return self.request('auth/r/margin/%s' % key, authenticate=True, params=endpoint_kwargs)

    def offers(self, **endpoint_kwargs):
        if self.REST.version == 'v1':
            return self.request('offers', authenticate=True, params=endpoint_kwargs)
        return self.request('auth/r/offers', authenticate=True, params=endpoint_kwargs)

    ########################
    # Version 1 Only Methods
    ########################

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def tickers(self):
        return self.request('tickers')

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def symbols(self, verbose=False):
        if verbose:
            return self.request('symbols_details')
        return self.request('symbols')

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def symbols_details(self):
        return self.request('symbols_details')

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def lends(self, currency, **endpoint_kwargs):
        return self.request('lends/%s' % currency, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def funding_book(self, currency, **endpoint_kwargs):
        return self.request('lendbook/%s' % currency, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def account_info(self):
        return self.request('account_infos', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def account_fees(self):
        return self.request('account_fees', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def summary(self):
        return self.request('summary', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def deposit(self, **endpoint_kwargs):
        return self.request('deposit', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def key_info(self):
        return self.request('key_info', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def funding_info(self, pair, **endpoint_kwargs):
        return self.request('auth/r/funding/%s' % pair, authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def balances(self):
        return self.request('balances', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def transfer(self, **endpoint_kwargs):
        return self.request('transfer', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def withdrawal(self, **endpoint_kwargs):
        return self.request('withdraw', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def new_order(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        payload = {'symbol': pair}
        payload.update(endpoint_kwargs)
        return self.request('order/new', authenticate=True, params=payload)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def multiple_new_orders(self, *orders):
        raise NotImplementedError

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def cancel_multiple_orders(self, *order_ids):
        return self.request('order/cancel/multi', authenticate=True,
                            params={'order_ids': order_ids})

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def cancel_all_orders(self):
        return self.request('order/cancel/all', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def replace_order(self, **endpoint_kwargs):
        return self.request('order/cancel/replace', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def active_orders(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.request('orders', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def active_positions(self):
        return self.request('positions', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def claim_position(self, **endpoint_kwargs):
        return self.request('position/claim', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def balance_history(self, **endpoint_kwargs):
        return self.request('history', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def deposit_withdrawal_history(self, **endpoint_kwargs):
        return self.request('history/movement', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def past_trades(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        payload = {'symbol': pair}
        payload.update(endpoint_kwargs)
        return self.request('mytrades', authenticate=True, params=payload)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def new_offer(self, **endpoint_kwargs):
        return self.request('offer/new', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def cancel_offer(self, **endpoint_kwargs):
        return self.request('offer/cancel', authenticate=False, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def offer_status(self, **endpoint_kwargs):
        return self.request('offer/status', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def active_credits(self, **endpoint_kwargs):
        return self.request('credits', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def taken_funds(self, **endpoint_kwargs):
        return self.request('taken_funds', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def unused_taken_funds(self, **endpoint_kwargs):
        return self.request('unused_taken_funds', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def total_taken_funds(self, **endpoint_kwargs):
        return self.request('total_taken_funds', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def close_funding(self, **endpoint_kwargs):
        return self.request('funding/close', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def basket_manage(self, **endpoint_kwargs):
        return self.request('basket_manage', authenticate=True, params=endpoint_kwargs)

    ########################
    # Version 2 Only Methods
    ########################
    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def candles(self, pair, **endpoint_kwargs):
        time_frame = endpoint_kwargs.pop('time_frame')
        section = endpoint_kwargs.pop('section')
        return self.request('candles/trade:%s:%s/%s' % (time_frame, pair, section),
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def market_average_price(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        return self.request('calc/trade/avg', data=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def wallets(self):
        return self.request('auth/r/wallets', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def orders(self):
        return self.request('auth/r/orders', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def order_trades(self, pair, order_id, **endpoint_kwargs):
        return self.request('auth/r/order/%s:%s/trades' % (pair, order_id),
                            authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def positions(self):
        return self.request('auth/r/positions', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def performance(self):
        return self.request('auth/r/stats/perf:1D/hist', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def alert_list(self, **endpoint_kwargs):
        price = endpoint_kwargs.pop('type')
        return self.request('auth/r/alerts?type=%s' % price, authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def alert_set(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        endpoint_kwargs['symbol'] = pair
        return self.request('auth/w/alert/set', authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def alert_delete(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        price = endpoint_kwargs.pop('price')
        return self.request('auth/w/alert/price:%s:%s/del' % (pair, price), authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def calc_available_balance(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        endpoint_kwargs['symbol'] = pair
        return self.request('auth/calc/order/avail', authenticate=True, params=endpoint_kwargs)
