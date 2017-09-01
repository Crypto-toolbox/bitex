# Import Built-Ins
import logging

# Import Third-Party
import requests

# Import Homebrew
from bitex.exceptions import UnsupportedPairError

from bitex.api.REST.rest import RESTAPI
from bitex.api.REST.bitfinex import BitfinexREST
from bitex.api.REST.bitstamp import BitstampREST
from bitex.api.REST.bittrex import BittrexREST
from bitex.api.REST.btce import BTCEREST
from bitex.api.REST.bter import BterREST
from bitex.api.REST.ccex import CCEXREST
from bitex.api.REST.coincheck import CoincheckREST
from bitex.api.REST.cryptopia import CryptopiaREST
from bitex.api.REST.gdax import GDAXREST
from bitex.api.REST.gemini import GeminiREST
from bitex.api.REST.hitbtc import HitBTCREST
from bitex.api.REST.itbit import ITbitREST
from bitex.api.REST.kraken import KrakenREST
from bitex.api.REST.okcoin import OKCoinREST
from bitex.api.REST.poloniex import PoloniexREST
from bitex.api.REST.quadriga import QuadrigaCXREST
from bitex.api.REST.quoine import QuoineREST
from bitex.api.REST.rocktrading import RockTradingREST
from bitex.api.REST.vaultoro import VaultoroREST
from bitex.api.REST.yunbi import YunbiREST

from bitex.interface.rest import RESTInterface
from bitex.utils import check_version_compatibility, check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitfinex(RESTInterface):
    """Bitfinex Interface class.

    Includes standardized methods, as well as all other Endpoints
    available on their REST API.
    """
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

    def __init__(self, **APIKwargs):
        super(Bitfinex, self).__init__('Bitfinex', BitfinexREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if not authenticate:
            return super(Bitfinex, self).request('GET', endpoint,
                                                 authenticate=authenticate,
                                                 **req_kwargs)
        else:
            return super(Bitfinex, self).request('POST', endpoint,
                                                 authenticate=authenticate,
                                                 **req_kwargs)

    def _get_supported_pairs(self):
        if self.REST.version == 'v1':
            return self.symbols().json()
        else:
            return requests.get('https://api.bitfinex.com/v1/symbols').json()

    ###############
    # Basic Methods
    ###############
    @check_and_format_pair
    def ticker(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('pubticker/%s' % pair)
        else:
            return self.request('ticker/%s' % pair,
                                params=endpoint_kwargs)

    @check_and_format_pair
    def order_book(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('book/%s' % pair,
                                params=endpoint_kwargs)
        else:
            prec = ('P0' if 'Precision' not in endpoint_kwargs else
                    endpoint_kwargs.pop('Precision'))
            return self.request('book/%s/%s' % (pair, prec),
                                params=endpoint_kwargs)

    @check_and_format_pair
    def trades(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.REST.version == 'v1':
            return self.request('trades/%s' % pair,
                                params=endpoint_kwargs)
        else:
            return self.request('trades/%s/hist' % pair,
                                params=endpoint_kwargs)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy', **kwargs)

    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'symbol': pair, 'price': price,
                   'amount': size, 'side': side, 'type': 'exchange-limit'}
        payload.update(kwargs)
        return self.new_order(pair, **payload)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def order_status(self, order_id, *args, **kwargs):
        return self.request('order/status', authenticate=True,
                            params={'order_id': order_id})

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
        else:
            key = endpoint_kwargs.pop('key')
            size = endpoint_kwargs.pop('size')
            side = endpoint_kwargs.pop('side')
            section = endpoint_kwargs.pop('section')
            path = key, size, pair, side, section
            return self.request('stats1/%s:%s:%s:%s/%s' % path,
                                params=endpoint_kwargs)

    def margin_info(self, **endpoint_kwargs):
        if self.REST.version == 'v1':
            return self.request('margin_info', authenticate=True)
        else:
            key = endpoint_kwargs.pop('key')
            return self.request('auth/r/margin/%s' % key, authenticate=True,
                                params=endpoint_kwargs)

    def offers(self, **endpoint_kwargs):
        if self.REST.version == 'v1':
            return self.request('offers', authenticate=True,
                                params=endpoint_kwargs)
        else:
            return self.request('auth/r/offers', authenticate=True,
                                params=endpoint_kwargs)

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
        else:
            return self.request('symbols')

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def symbols_details(self):
        return self.request('symbols_details')

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def lends(self, currency, **endpoint_kwargs):
        return self.request('lends/%s' % currency,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def funding_book(self, currency, **endpoint_kwargs):
        return self.request('lendbook/%s' % currency,
                            params=endpoint_kwargs)

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
        return self.request('deposit', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def key_info(self):
        return self.request('key_info', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def funding_info(self, **endpoint_kwargs):
        return self.request('auth/r/funding/%s' % key, authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def balances(self):
        return self.request('balances', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def transfer(self, **endpoint_kwargs):
        return self.request('transfer', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def withdrawal(self, **endpoint_kwargs):
        return self.request('withdraw', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def new_order(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        payload = {'symbol': pair}
        payload.update(endpoint_kwargs)
        return self.request('order/new', authenticate=True,
                            params=payload)

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
        return self.request('order/cancel/replace', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def active_orders(self, *args, **kwargs):
        return self.request('orders', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def active_positions(self):
        return self.request('positions', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def claim_position(self, **endpoint_kwargs):
        return self.request('position/claim', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def balance_history(self, **endpoint_kwargs):
        return self.request('history', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def deposit_withdrawal_history(self, **endpoint_kwargs):
        return self.request('history/movement', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def past_trades(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        payload = {'symbol': pair}
        payload.update(endpoint_kwargs)
        return self.request('mytrades', authenticate=True,
                            params=payload)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def new_offer(self, **endpoint_kwargs):
        return self.request('offer/new', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def cancel_offer(self, **endpoint_kwargs):
        return self.request('offer/cancel', authenticate=False,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def offer_status(self, **endpoint_kwargs):
        return self.request('offer/status', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def active_credits(self, **endpoint_kwargs):
        return self.request('credits', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def taken_funds(self, **endpoint_kwargs):
        return self.request('taken_funds', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def unused_taken_funds(self, **endpoint_kwargs):
        return self.request('unused_taken_funds', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def total_taken_funds(self, **endpoint_kwargs):
        return self.request('total_taken_funds', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def close_funding(self, **endpoint_kwargs):
        return self.request('funding/close', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def basket_manage(self, **endpoint_kwargs):
        return self.request('basket_manage', authenticate=True,
                            params=endpoint_kwargs)

    ########################
    # Version 2 Only Methods
    ########################
    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def candles(self, pair, **endpoint_kwargs):
        time_frame = endpoint_kwargs.pop('time_frame')
        section = endpoint_kwargs.pop('section')
        return self.request('candles/trade:%s:%s/%s' %
                            (time_frame, pair, section),
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
        return self.request('auth/r/order/%s:%s/trades' %
                            (pair, order_id),
                            authenticate=True, params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def positions(self):
        return self.request('auth/r/positions', authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    def offers(self):
        return self.request('auth/offers', authenticate=True)

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
        return self.request('auth/w/alert/set', authenticate=True,
                            params=endpoint_kwargs)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def alert_delete(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        symbol = endpoint_kwargs.pop('price')
        return self.request('auth/w/alert/price:%s:%s/del' %
                            (pair, price),
                            authenticate=True)

    @check_version_compatibility(v1=v1_only_methods, v2=v2_only_methods)
    @check_and_format_pair
    def calc_available_balance(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        endpoint_kwargs['symbol'] = pair
        return self.request('auth/calc/order/avail', authenticate=True,
                            params=endpoint_kwargs)


class Bitstamp(RESTInterface):
    """Bitstamp REST API Interface Class.

    Since Bitstamp doesn't make an explicit differentiation between api versions,
    we do not use a version checker for this interface.
    """
    def __init__(self, **APIKwargs):
        super(Bitstamp, self).__init__('Bitstamp', BitstampREST(**APIKwargs))

    def _get_supported_pairs(self):
        return ['btceur', 'btcusd', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc',
                'ltcusd', 'ltceur', 'ltcbtc']

    def request(self, endpoint, authenticate=False, **kwargs):
        verb = 'POST' if authenticate else 'GET'
        return super(Bitstamp, self).request(verb, endpoint,
                                             authenticate=authenticate, **kwargs)

    ###############
    # Basic Methods
    ###############

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('ticker/%s/' % pair,
                            params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('order_book/%s/' % pair,
                            params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('transactions/%s/' % pair,
                            params=kwargs)

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, market=False, **kwargs):
        return self._place_order(pair, price, size, 'buy', market=market,
                                 **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, market=False, **kwargs):
        return self._place_order(pair, price, size, 'buy', market=False,
                                 **kwargs)

    def _place_order(self, pair, size, price, side, market=None):
        payload = {'amount': size, 'price': price}
        payload.update(kwargs)
        if market:
                    return self.request('%s/market/%s/' %
                                        (side, pair),
                                         authenticate=True, data=payload)
        else:
            return self.request('%s/%s/' % (side, pair),
                                authenticate=True, data=payload)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'id': order_id}
        payload.update(kwargs)
        return self.request('api/order_status/', authenticate=True,
                            data=payload)

    def open_orders(self, *args, pair=None, **kwargs):
        if pair:
            return self.request('open_orders/%s/' % pair,
                                authenticate=True, data=kwargs)
        else:
            return self.request('open_orders/all/', authenticate=True,
                                data=kwargs)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'id': oid})
            r = self.request('cancel_order/', authenticate=True, data=payload)
            results.append(r)
        return results if len(results) > 1 else results[0]


    def wallet(self, *args, **kwargs):
        pair = kwargs['pair'].format_for(self.name).lower() if 'pair' in kwargs else None
        if pair:
            return self.request('balance/%s/' % pair,
                                authenticate=True, data=kwargs)
        else:
            return self.request('balance/', authenticate=True, data=kwargs)

    ###########################
    # Exchange Specific Methods
    ###########################

    @check_and_format_pair
    def hourly_ticker(self, pair, **kwargs):
        if pair:
            return self.request('ticker_hour/%s/' % pair,
                                params=kwargs)
        else:
            return self.request('api/ticker_hour/')

    def eur_usd_conversion_rate(self, **kwargs):
        return self.request('api/eur_usd/', params=kwargs)

    @check_and_format_pair
    def user_transactions(self, pair, **kwargs):
        if pair:
            return self.request('user_transactions/%s/' %
                                pair, authenticate=True,
                                data=kwargs)
        else:
            return self.request('api/user_transactions/', authenticate=True,
                                data=kwargs)

    def cancel_all_orders(self, **kwargs):
        return self.request('api/cancel_all_orders/', authenticate=True,
                            data=kwargs)

    def withdrawal_request(self, **kwargs):
        return self.request('api/withdrawal_request', authenticate=True,
                            data=kwargs)

    def withdraw(self, currency, **kwargs):
        if currency in ('LTC', 'ltc'):
            return self.request('ltc_withdrawal', authenticate=True)
        elif currency in ('BTC', 'btc'):
            return self.request('api/bitcoin_widthdrawal', authenticate=True)
        elif currency in ('XRP', 'xrp'):
            return self.request('xrp_withdrawal/', authenticate=True)
        else:
            raise UnsupportedPairError('Currency must be LTC/ltc,'
                                       'BTC/btc or XRP/xrp!')

    def deposit_address(self, currency):
        if currency in ('LTC', 'ltc'):
            return self.request('ltc_address/', authenticate=True)
        elif currency in ('BTC', 'btc'):
            return self.request('api/bitcoin_deposit_address', authenticate=True)
        elif currency in ('XRP', 'xrp'):
            return self.request('xrp_address/', authenticate=True)
        else:
            raise UnsupportedPairError('Currency must be LTC/ltc or BTC/btc!')

    def unconfirmed_bitcoin_deposits(self):
        return self.request('api/unconfirmed_btc/', authenticate=True)

    def transfer_sub_to_main(self, **kwargs):
        return self.request('transfer_to_main/', authenticate=True,
                            data=kwargs)

    def transfer_main_to_sub(self, **kwargs):
        return self.request('transfer_from_main/', authenticate=True,
                            data=kwargs)

    def open_bank_withdrawal(self, **kwargs):
        return self.request('withdrawal/open/', authenticate=True, data=kwargs)

    def bank_withdrawal_status(self, **kwargs):
        return self.request('withdrawal/status/', authenticate=True,
                            data=kwargs)

    def cancel_bank_withdrawal(self, **kwargs):
        return self.request('withdrawal/cancel/', authenticate=True,
                            data=kwargs)

    def liquidate(self, **kwargs):
        return self.request('liquidation_address/new/', authenticate=True,
                            data=kwargs)

    def liquidation_info(self, **kwargs):
        return self.request('liquidation_address/info/', authenticate=True,
                            data=kwargs)


class Bittrex(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Bittrex, self).__init__('Bittrex', BittrexREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        return super(Bittrex, self).request('GET', endpoint, authenticate,
                                            **req_kwargs)

    def _get_supported_pairs(self):
        r = self.pairs()
        pairs = [item['MarketName'] for item in r.json()['result']]
        return pairs

    ###############
    # Basic Methods
    ###############
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        payload = {'market': pair}
        payload.update(kwargs)
        return self.request('public/getmarketsummary', params=payload)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'market': pair, 'type': 'both'}
        payload.update(kwargs)
        return self.request('public/getorderbook', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'market': pair}
        payload.update(kwargs)
        return self.request('public/getmarkethistory', params=payload)

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        payload = {'market': pair, 'quantity': size, 'rate': price}
        payload.update(kwargs)
        return self.request('market/selllimit', params=payload,
                            authenticate=True)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        payload = {'market': pair, 'quantity': size, 'rate': price}
        payload.update(kwargs)
        return self.request('market/buylimit', params=payload,
                            authenticate=True)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'uuid': order_id}
        payload.update(kwargs)
        return self.request('account/getorder', params=payload,
                            authenticate=True)

    def open_orders(self, *args, **kwargs):
        return self.request('market/getopenorders', params=kwargs,
                            authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for uuid in order_ids:
            payload.update({'uuid': uuid})
            r = self.request('market/cancel', params=payload,
                             authenticate=True)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, currency=None, *args, **kwargs):
        if currency:
            payload = {'currency': currency}
            payload.update(kwargs)
            return self.request('account/getbalance', params=payload,
                                authenticate=True)
        else:
            payload = kwargs
            return self.request('account/getbalances', params=payload,
                                authenticate=True)

    ###########################
    # Exchange Specific Methods
    ###########################

    def deposit_address(self, currency, **kwargs):
        payload = {'currency': currency}
        payload.update(kwargs)
        return self.request('account/getdepositaddress', params=payload,
                            authenticate=True)

    def withdraw(self, **kwargs):
        return self.request('account/withdraw', params=kwargs)

    def trade_history(self, *args, **kwargs):
        return self.request('account/getorderhistory', params=kwargs)

    def withdrawal_history(self, *args, **kwargs):
        return self.request('account/getwithdrawalhistory', params=kwargs)

    def deposit_history(self, *args, **kwargs):
        return self.request('account/getdeposithistory', params=kwargs)

    def pairs(self, **kwargs):
        return self.request('public/getmarkets', params=kwargs)

    def currencies(self, **kwargs):
        return self.request('public/getcurrencies', params=kwargs)

    def simple_ticker(self, **kwargs):
        return self.request('public/getticker', params=kwargs)


class BTCE(RESTInterface):
    def __init__(self, **APIKwargs):
        super(BTCE, self).__init__('BTC-E', BTCEREST(**APIKwargs))

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('GET', 'ticker/%s' % pair)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('GET', 'depth/%s' % pair)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('GET', 'trades/%s' % pair)

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell')

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy')

    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'pair': pair, 'type': side, 'rate': price, 'amount': size}
        payload.update(kwargs)
        return self.request('POST', 'Trade', params=payload, authenticate=True)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'order_id': order_id}
        payload.update(kwargs)
        return self.request('POST', 'OrderInfo', params=payload,
                            authenticate=True)

    @check_and_format_pair
    def open_orders(self, *args, **kwargs):
        return self.request('POST', 'ActiveOrders', params=kwargs,
                            authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        result = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'order_id': oid})
            r = self.request('POST', 'CancelOrder', params=payload,
                             authenticate=True)
            result.append(r)
        return result if len(result) > 1 else r[0]

    def wallet(self, *args, **kwargs):
        return self.request('POST', 'getInfo', authenticate=True)


class Bter(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Bter, self).__init__('Bter', BterREST(**APIKwargs))

    def _get_supported_pairs(self):
        return self.request('GET', 'pairs').json()

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('GET', 'ticker/%s' % pair)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('GET', 'orderBook/%s' % pair)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        tid = '' if not 'TID' in kwargs else '/' + str(kwargs['TID'])
        return self.request('GET', 'tradeHistory' + tid)

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_orde(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_orde(pair, price, size, 'buy', **kwargs)

    def _place_orde(self, pair, price, size, side, **kwargs):
        payload = {'currencyPair': pair, 'rate': price, 'amount': size}
        payload.update(kwargs)
        return self.request('POST', 'private/%s' % side, authenticate=True,
                            params=payload)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'orderNumber': order_id}
        payload.update(kwargs)
        return self.request('POST', 'private/getOrder', params=payload,
                            authenticate=True)

    def open_orders(self, *args, **kwargs):
        return self.request('POST', 'private/openOrders', authenticate=True)

    def cancel_order(self, *order_ids, cancel_all=False, **kwargs):
        if cancel_all:
            return self.request('POST', 'private/cancelAllOrders', params=kwargs,
                                authenticate=True)
        else:
            results = []
            payload = kwargs
            for oid in order_ids:
                payload.update({'orderNumber': oid})
                results.append(self.request('POST', 'private/cancelOrder',
                                            params=payload, authenticate=True))
            return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('POST', 'private/balances', authenticate=True)


class CCEX(RESTInterface):
    def __init__(self, **APIKwargs):
        super(CCEX, self).__init__('C-CEX', CCEXREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if authenticate:
            endpoint = endpoint if endpoint else 'api.html'
            return super(CCEX, self).request('GET', endpoint, authenticate=True,
                                **req_kwargs)
        else:
            endpoint = endpoint if endpoint else 'api_pub.html'
            return super(CCEX, self).request('GET', endpoint, **req_kwargs)

    def _get_supported_pairs(self):
        return requests.get('https://c-cex.com/t/pairs.json').json()['pairs']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('%s.json' % pair, params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'a': 'getorderbook', 'market': pair, 'type': 'both'}
        payload.update(kwargs)
        return self.request(None, params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'a': 'getmarkethistory', 'market': pair}
        payload.update(kwargs)
        return self.request(None, params=payload)

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        payload = {'a': 'selllimit', 'market': pair, 'quantity': size,
                   'rate': price}
        payload.update(kwargs)
        return self.request(None, authenticate=True, params=payload)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        payload = {'a': 'buylimit', 'market': pair, 'quantity': size,
                   'rate': price}
        payload.update(kwargs)
        return self.request(None, authenticate=True, params=payload)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'a': 'getorder', 'uuid': order_id}
        payload.update(kwargs)
        return self.request(None, params=payload, authenticate=True)

    def open_orders(self, *args, **kwargs):
        payload = {'a': 'getopenorders'}
        payload.update(kwargs)
        return self.request(None, params=payload, authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        payload = {'a': 'cancel'}
        payload.update(kwargs)
        results = []
        for oid in order_ids:
            payload.update({'uuid': oid})
            results.append(self.request(None, params=payload,
                                        authenticate=True))
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, currency=None, **kwargs):
        if currency:
            payload = {'a': 'getbalance'}
            payload.update(kwargs)
            payload.update({'currency': currency})
        else:
            payload = {'a': 'getbalances'}
            payload.update(kwargs)
        return self.request(None, params=payload, authenticate=True)


class CoinCheck(RESTInterface):
    """Interface Class for the Coincheck.com REST API.

    Documentation:
        https://coincheck.com/documents/exchange/api

    The API documentation appears to be not up-to-date, or the endpoints
    not updated to support the various new pairs at the exchange.

    """
    def __init__(self, **APIKwargs):
        super(CoinCheck, self).__init__('CoinCheck',
                                        CoincheckREST(**APIKwargs))

    def _get_supported_pairs(self):
        return ['btc-jpy']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('GET', 'ticker', params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('GET', 'order_books', params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('GET', 'trades', params=kwargs)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'rate': price, 'amount': size, 'pair': pair,
                   'order_type': side}
        payload.update(kwargs)
        return self.request('POST', 'exchange/orders', params=payload,
                            authenticate=True)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        if 'order_type' in kwargs:
            if (kwargs['order_type'] not in
                    ('sell', 'market_sell', 'leverage_sell', 'close_short')):
                raise ValueError("order_type not supported by this function!")
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        if 'order_type' in kwargs:
            if (kwargs['order_type'] not in
                    ('buy', 'market_buy', 'leverage_buy', 'close_long')):
                raise ValueError("order_type not supported by this function!")
        return self._place_order(pair, price, size, 'sell', **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        return self.request('GET', 'exchange/orders/open', params=kwargs,
                            authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        result = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'order_id': oid})
            r = self.request('DELETE', 'exchange/orders/' + oid,
                             params=payload, authenticate=True)
            result.append(r)
        return r if len(r) > 1 else r[0]

    def wallet(self, *args, **kwargs):
        return self.request('GET', 'accounts/balance', params=kwargs,
                            authenticate=True)


class Cryptopia(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Cryptopia, self).__init__('Cryptopia', CryptopiaREST(**APIKwargs))

    def _get_supported_pairs(self):
        r = self.request('GET', 'GetTradePairs').json()
        pairs = [entry['Label'].replace('/', '_') for entry in r['Data']]
        return pairs

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('GET', 'GetMarket/' + pair, params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('GET', 'GetMarketOrders/' + pair, params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('GET', 'GetMarketHistory/' + pair, params=kwargs)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, *args, **kwargs):
        payload = {'Market': pair, 'Type': side, 'Rate': price, 'Amount': size}
        payload.update(kwargs)
        return self.request('POST', 'SubmitTrade', params=payload,
                            authenticate=True)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'Sell', *args, **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'Buy', *args, **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        return self.request('POST', 'GetOpenOrders', params=kwargs,
                            authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = {'Type': 'Trade'}
        for oid in order_ids:
            payload.update({'OrderId': oid})
            r = self.request('POST', 'CancelTrade', params=payload,
                             authenticate=True)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('POST', 'GetBalance', params=kwargs,
                            authenticate=True)


class HitBTC(RESTInterface):
    def __init__(self, **APIKwargs):
        super(HitBTC, self).__init__('HitBTC', HitBTCREST(**APIKwargs))

    def _get_supported_pairs(self):
        r = self.request('symbols')
        return [entry['symbol'] for entry in r.json()['symbols']]

    def request(self, endpoint, authenticate=False, verb=None, **req_kwargs):
        verb = verb if verb else 'GET'
        if authenticate:
            endpoint = 'trading/' + endpoint
        else:
            endpoint = 'public/' + endpoint
        return super(HitBTC, self).request(verb, endpoint, authenticate,
                                           **req_kwargs)

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('%s/ticker' % pair, params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('%s/orderbook' % pair, params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        if 'from' not in kwargs:
            return self.request('%s/trades/recent' % pair, params=kwargs)
        else:
            return self.request('%s/trades', params=kwargs)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, *args, **kwargs):
        payload = {'symbol': pair, 'side': side, 'price': price,
                   'quantity': size, 'type': 'limit'}
        payload.update(kwargs)
        return self.request('new_order', authenticate=True, verb='POST',
                            params=kwargs)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell')

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy')

    def order_status(self, order_id, *args, **kwargs):
        payload = {'client_order_id': order_id}
        payload.update(kwargs)
        return self.request('order', params=payload, authenticate=True)

    def open_orders(self, *args, **kwargs):
        return self.request('orders/active', authenticate=True, params=kwargs)

    def cancel_order(self, *order_ids, cancel_all=False, **kwargs):
        if cancel_all:
            return self.request('cancel_orders', authenticate=True, verb='POST',
                                params=kwargs)
        else:
            results = []
            payload = kwargs
            for oid in order_ids:
                payload.update({'clientOrderId': oid})
                r = self.request('cancel_order', authenticate=True,
                                 verb='POST', params=payload)
                results.append(r)
            return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('balance', authenticate=True, params=kwargs)


class Kraken(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Kraken, self).__init__('Kraken', KrakenREST(**APIKwargs))

    def _get_supported_pairs(self):
        r = self.request('AssetPairs').json()['result']
        return [r[k]['base'] + r[k]['quote'] if r[k]['base'] != 'BCH'
                else k for k in r]

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if authenticate:
            return super(Kraken, self).request('POST', 'private/' + endpoint,
                                               authenticate=True, **req_kwargs)
        else:
            return super(Kraken, self).request('GET', 'public/' + endpoint, **req_kwargs)

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, *pairs, **kwargs):
        payload = {'pair': pairs}
        payload.update(kwargs)
        return self.request('Ticker', params=payload)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'pair': pair}
        payload.update(kwargs)
        return self.request('Depth', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'pair': pair}
        payload.update(kwargs)
        return self.request('Trades', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'pair': pair, 'type': side, 'ordertype': 'limit',
                   'price': price, 'volume': size}
        payload.update(kwargs)
        return self.request('AddOrder', authenticate=True, data=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy', **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        return self.request('OpenOrders', authenticate=True, data=kwargs)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'txid': oid})
            r = self.request('CancelOrder', authenticate=True, data=payload)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('Balance', authenticate=True, data=kwargs)


class OKCoin(RESTInterface):
    def __init__(self, **APIKwargs):
        super(OKCoin, self).__init__('OKCoin', OKCoinREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if authenticate:
            return super(OKCoin, self).request('POST', endpoint, authenticate,
                                               **req_kwargs)
        else:
            return super(OKCoin, self).request('GET', endpoint, authenticate,
                                               **req_kwargs)

    def _get_supported_pairs(self):
        return ['btc_usd', 'ltc_usd', 'eth_usd',
                'btc_cny', 'ltc_cny', 'eth_cny']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        payload = {'symbol': pair}
        payload.update(kwargs)
        return self.request('ticker.do', params=payload)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'symbol': pair}
        payload.update(kwargs)
        return self.request('depth.do', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'symbol': pair}
        payload.update(kwargs)
        return self.request('trades.do', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'symbol': pair, 'type': side, 'price': price, 'amount': size}
        payload.update(kwargs)
        return self.request('trade.do', authenticate=True, params=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell')

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy')

    def order_status(self, order_id, *args, **kwargs):
        payload = {'order_id': order_id}
        payload.update(kwargs)
        return self.request('order_info.do', authenticate=True, params=payload)

    def open_orders(self, *args, **kwargs):
        return self.order_status(-1, **kwargs)

    def cancel_order(self, *order_ids, **kwargs):
        payload = kwargs
        payload.update({'order_id': ','.join(list(order_ids))})
        return self.request('cancel_order.do', authenticate=True, params=payload)

    def wallet(self, *args, **kwargs):
        return self.request('userinfo.do', authenticate=True, params=kwargs)


class Poloniex(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Poloniex, self).__init__('Poloniex', PoloniexREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if 'params' in req_kwargs:
            req_kwargs['params'].update({'command': endpoint})
        else:
            req_kwargs['params'] = {'command': endpoint}
        if authenticate:
            return super(Poloniex, self).request('POST', endpoint, authenticate,
                                                 **req_kwargs)
        else:
            return super(Poloniex, self).request('GET', 'public', authenticate,
                                                 **req_kwargs)

    def _get_supported_pairs(self):
        return ['BTC_ETH']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('returnTicker', params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'currencyPair': pair}
        payload.update(kwargs)
        return self.request('returnOrderBook', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'currencyPair': pair}
        payload.update(kwargs)
        return self.request('returnTradeHistory', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'currencyPair': pair, 'rate': price, 'amount': size}
        payload.update(kwargs)
        if side == 'bid':
            return self.request('buy', authenticate=True, params=payload)
        else:
            return self.request('sell', authenticate=True, params=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        payload = {'orderNumber': order_id}
        payload.update(kwargs)
        return self.request('returnOrderTrades', authenticate=True,
                            params=payload)

    def open_orders(self, *args, **kwargs):
        payload = {'currencyPair': 'all'}
        payload.update(kwargs)
        return self.request('returnOpenOrders', authenticate=True,
                            params=payload)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'orderNumber', oid})
            r = self.request('cancelOrder', authenticate=True, params=oid)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('returnTradableBalances', authenticate=True,
                            params=kwargs)


class QuadrigaCX(RESTInterface):
    def __init__(self, **APIKwargs):
        super(QuadrigaCX, self).__init__('QuadrigaCX',
                                         QuadrigaCXREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        if authenticate:
            return super(QuadrigaCX, self).request('POST', endpoint,
                                                   authenticate, **req_kwargs)
        else:
            return super(QuadrigaCX, self).request('GET', endpoint,
                                                   authenticate, **req_kwargs)

    def _get_supported_pairs(self):
        return ['btc_cad', 'btc_usd', 'eth_btc', 'eth_cad']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        payload = {'book': pair}
        payload.update(kwargs)
        return self.request('ticker', params=payload)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'book': pair}
        payload.update(kwargs)
        return self.request('order_book', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'book': pair}
        payload.update(kwargs)
        return self.request('transactions', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'price': price, 'amount': size, 'book': pair}
        payload.update(kwargs)
        return self.request(side, authenticate=True, params=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy', **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'id': order_id}
        payload.update(kwargs)
        return self.request('lookup_order', authenticate=True, params=payload)

    def open_orders(self, *args, **kwargs):
        return self.request('open_orders', authenticate=True, params=kwargs)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'id': oid})
            r = self.request('cancel_order', authenticate=True, params=payload)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('balance', authenticate=True, params=kwargs)


class TheRockTrading(RESTInterface):
    def __init__(self, **APIKwargs):
        super(TheRockTrading, self).__init__('The Rock Trading Ltd.',
                                             RockTradingREST(**APIKwargs))

    def _get_supported_pairs(self):
        return [d['id'] for d in self.request('GET', 'funds').json()['funds']]

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('GET', 'funds/%s/ticker' % pair, params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('GET', 'funds/%s/orderbook' % pair, params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('GET', 'funds/%s/trades' % pair, params=kwargs)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'price': price, 'amount': size, 'side': side}
        payload.update(kwargs)
        return self.request('POST', 'funds/%s/orders' % pair, authenticate=True,
                            params=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy', **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        if 'pair' not in kwargs and 'fund_id' not in kwargs:
            raise ValueError("Need to specify pair or fund_id in kwargs!")
        else:
            try:
                pair = kwargs.pop('pair')
            except KeyError:
                pair = kwargs.pop('fund_id')
            return self.request('GET', 'funds/%s/orders/%s' % (pair, order_id),
                                authenticate=True, params=kwargs)

    def open_orders(self, *args, **kwargs):
        if 'pair' not in kwargs and 'fund_id' not in kwargs:
            results = []
            for fund_id in self.supported_pairs:
                r = self.request('GET', 'funds/%s/orders' % fund_id,
                                 authenticate=True, params=kwargs)
                results.append(r)
            return results if len(results) > 1 else results[0]
        else:
            try:
                pair = kwargs.pop('pair')
            except KeyError:
                pair = kwargs.pop('fund_id')

            return self.request('GET', 'funds/%s/orders' % pair,
                                authenticate=True, params=kwargs)

    def cancel_order(self, *order_ids, all=False, **kwargs):
        results = []
        if 'pair' not in kwargs and 'fund_id' not in kwargs:
            for fund_id in self.supported_pairs:
                r = self.cancel_order(*order_ids, all, pair=fund_id)
                results.append(r)
            return results if len(results) > 1 else results[0]
        else:
            try:
                pair = kwargs.pop('pair')
            except KeyboardInterrupt:
                pair = kwargs.pop('fund_id')

        if all:
            return self.request('DELETE', 'funds/%s/orders/remove_all' % pair,
                                authenticate=True, params=kwargs)
        else:
            for oid in order_ids:
                r = self.request('DELETE', 'funds/%s/orders/%s' % (pair, oid),
                                 authenticate=True, params=kwargs)
                results.append(r)
            return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('GET', 'balances', authenticate=True, params=kwargs)


class Vaultoro(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Vaultoro, self).__init__('Vaultoro', VaultoroREST(**APIKwargs))

    def request(self, endpoint, authenticate=False, post=False, **req_kwargs):
        verb = 'GET' if not post else 'POST'
        return super(Vaultoro, self).request(verb, endpoint, authenticate, **req_kwargs)

    def _get_supported_pairs(self):
        return ['BTC-GLD']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('https://api.vaultoro.com/markets', params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('https://api.vaultoro.com/orderbook/', params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('https://api.vaultoro.com/latesttrades', params=kwargs)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, market_order, **kwargs):
        order_type = 'limit' if not market_order else 'market'
        q = {'gld': size, 'price': price}
        return self.request('https://api.vaultoro.com/1/%s/gld/%s' %
                            (side, order_type), authenticate=True,
                            post=True, params=q)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, market_order=False, **kwargs):
        return self._place_order(pair, price, size, 'sell', market_order,
                                 **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, market_order=False, **kwargs):
        return self._place_order(pair, price, size, 'buy', market_order,
                                 **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        return self.request('https://api.vaultoro.com/1/orders',
                            authenticate=True, params=kwargs)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        for oid in order_ids:
            r = self.request('https://api.vaultoro.com/1/cancel/%s' % oid,
                             authenticate=True, post=True, params=kwargs)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('https://api.vaultoro.com/1/balance',
                            authenticate=True, params=kwargs)
