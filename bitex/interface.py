# Import Built-Ins
import logging
import warnings
from functools import wraps
# Import Third-Party

# Import Homebrew
from .pairs import PairFormatter
from .exceptions import UnsupportedPairError, EmptySupportedPairListWarning
from .exceptions import UnsupportedEndpointError
from .rest import BitfinexREST, BittrexREST, BitstampREST, BTCEREST, BterREST
from .rest import CCEXREST, CoincheckREST, CryptopiaREST
from .rest import HitBTCREST, KrakenREST, OKCoinREST, PoloniexREST
from .rest import QuadrigaCXREST, RockTradingREST, VaultoroREST
# Init Logging Facilities
log = logging.getLogger(__name__)


class Interface:
    def __init__(self, *, name, rest_api):
        self.REST = rest_api
        self.name = name
        try:
            self._supported_pairs = self._get_supported_pairs()
        except NotImplementedError:
            self._supported_pairs = None

    @property
    def supported_pairs(self):
        return self._supported_pairs

    def _get_supported_pairs(self):
        """Generate a list of supported pairs.

        Queries the API for a list of supported pairs and returns this as a
        list.

        Raises a NotImplementedError by default and needs to be overridden in
        child classes.

        :raises: NotImplementedError
        """
        raise NotImplementedError

    def is_supported(self, pair):
        """Checks if the given pair is present in self._supported_pairs.

        Input can either be a string or a PairFormatter Obj (or child thereof).
        If the latter two, we'll call the format() method with the Interface's
        name attribute to acquire proper formatting.
        Since str.format() doesn't raise an error if a string isnt used,
        this works for both PairFormatter objects and strings.
        :param pair: Str, or PairFormatter Object
        :return: Bool
        """
        try:
            pair = pair.format_for(self.name)
        except AttributeError:
            pair = pair

        if pair in self.supported_pairs:
            return True
        else:
            return False

    def request(self, verb, endpoint, authenticate=False, **req_kwargs):
        """Query the API and return its result.

        :param verb: HTTP verb (GET, PUT, DELETE, etc)
        :param endpoint: Str
        :param authenticate: Bool, whether to call private_query or public_query
                             method.
        :param req_kwargs: Kwargs to pass to _query / requests.request()
        :raise: UnsupportedPairError
        :return: requests.Response() Obj
        """

        if authenticate:
            return self.REST.private_query(verb, endpoint, **req_kwargs)
        else:
            return self.REST.public_query(verb, endpoint, **req_kwargs)


class RESTInterface(Interface):
    def __init__(self, name, rest_api):
        super(RESTInterface, self).__init__(name=name, rest_api=rest_api)

    # Public Endpoints
    def ticker(self, pair, *args, **kwargs):
        raise NotImplementedError

    def order_book(self, pair, *args, **kwargs):
        raise NotImplementedError

    def trades(self, pair, *args, **kwargs):
        raise NotImplementedError

    # Private Endpoints
    def ask(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    def bid(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        raise NotImplementedError

    def cancel_order(self, *order_ids, **kwargs):
        raise NotImplementedError

    def wallet(self, currency, *args, **kwargs):
        raise NotImplementedError


class Bitfinex(RESTInterface):
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

    @staticmethod
    @wraps
    def check_version_compatibility(func, *args, **kwargs):
        v2_endpoints = ['wallets', 'orders', 'order_trades', 'positions',
                        'offers', 'funding_info', 'performance', 'alert_list',
                        'alert_set', 'alert_delete', 'calc_available_balance',
                        'market_average_price', 'candles', 'ticker', 'tickers']
        def wrapper(*args, **kwargs):
            if func.__name__ in v2_endpoints and args[0].api.version != 'v2':
                raise UnsupportedEndpointError('This endpoint is only available for'
                                               'api version v2 (current is %s)'
                                               % self.api.version)
            elif func.__name__ not in v2_endpoints and args[0].api.version == 'v2':
                raise UnsupportedEndpointError('This endpoint is only available for'
                                               'api version v1 (current is %s)'
                                               % self.api.version)
            else:
                return func(*args, **kwargs)
        return wrapper

    def _get_supported_pairs(self):
        return self.symbols()

    ###############
    # Basic Methods
    ###############
    def ticker(self, pair):
        self.is_supported(pair)
        if self.api.version == 'v1':
            return self.request('pubticker/%s' % pair.format_for(self.name))
        else:
            return self.request('ticker/%s' % pair.format_for(self.name),
                                params=endpoint_kwargs)

    def order_book(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.api.version == 'v1':
            return self.request('book/%s' % pair.format_for(self.name),
                                params=endpoint_kwargs)
        else:
            prec = ('P0' if 'Precision' not in endpoint_kwargs else
                    endpoint_kwargs.pop('Precision'))
            return self.request('book/%s/%s' % (pair.format_for(self.name), prec),
                                params=endpoint_kwargs)

    def trades(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.api.version == 'v1':
            return self.request('trades/%s' % pair.format_for(self.name),
                                params=endpoint_kwargs)
        else:
            return self.request('trades/%s/hist' % pair.format_for(self.name),
                                params=endpoint_kwargs)

    def ask(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'sell', **kwargs)

    def bid(self, pair, price, size, *args, **kwargs):
        return self._place_order(pair, price, size, 'buy', **kwargs)

    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'symbol': pair.format_for(self.name), 'price': price,
                   'amount': size, 'side': side, 'type': 'exchange-limit'}
        payload.update(kwargs)
        return self.new_order(pair, **payload)

    def order_status(self, order_id, *args, **kwargs):
        return self.request('order/status', authenticate=True,
                            params={'order_id': order_id})

    def open_orders(self, *args, **kwargs):
        return self.active_orders(*args, **kwargs)

    def cancel_order(self, order_id, **kwargs):
        return self.request('order/cancel', authenticate=True,
                            params={'order_id': order_id})

    def wallet(self, *args, **kwargs):
        return self.balances()


    ###########################
    # Exchange Specific Methods
    ###########################
    @Bitfinex.check_version_compatibility
    def symbols(self, verbose=False):
        if verbose:
            return self.request('symbols_details')
        else:
            return self.request('symbols')

    @Bitfinex.check_version_compatibility
    def symbols_details(self):
        return self.request('symbols_details')


    def stats(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        if self.api.version == 'v1':
            return self.request('stats/%s' % pair.format_for(self.name))
        else:
            key = endpoint_kwargs.pop('key')
            size = endpoint_kwargs.pop('size')
            side = endpoint_kwargs.pop('side')
            section = endpoint_kwargs.pop('section')
            path = key, size, pair, side, section
            return self.request('stats1/%s:%s:%s:%s/%s' % path,
                                params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def candles(self, pair, **endpoint_kwargs):
        time_frame = endpoint_kwargs.pop('time_frame')
        section = endpoint_kwargs.pop('section')
        return self.request('candles/trade:%s:%s/%s' %
                            (time_frame, pair.format_for(self.name), section),
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def lends(self, currency, **endpoint_kwargs):
        return self.request('lends/%s' % currency,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def funding_book(self, currency, **endpoint_kwargs):
        return self.request('lendbook/%s' % currency,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def market_average_price(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        return self.request('calc/trade/avg', data=**endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def wallets(self):
        return self.request('auth/r/wallets', authenticate=True)

    @Bitfinex.check_version_compatibility
    def account_info(self):
        return self.request('account_infos', authenticate=True)

    @Bitfinex.check_version_compatibility
    def account_fees(self):
        return self.request('account_fees', authenticate=True)

    @Bitfinex.check_version_compatibility
    def summary(self):
        return self.request('summary', authenticate=True)

    @Bitfinex.check_version_compatibility
    def deposit(self, **endpoint_kwargs):
        return self.request('deposit', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def key_info(self):
        return self.request('key_info', authenticate=True)

    def margin_info(self, **endpoint_kwargs):
        if self.api.version == 'v1':
            return self.request('margin_info', authenticate=True)
        else:
            key = endpoint_kwargs.pop('key')
            return self.request('auth/r/margin/%s' % key, authenticate=True,
                                params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def funding_info(self, **endpoint_kwargs):
        return self.request('auth/r/funding/%s' key, authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def balances(self):
        return self.request('balances', authenticate=True)

    @Bitfinex.check_version_compatibility
    def transfer(self, **endpoint_kwargs):
        return self.request('transfer', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def withdrawal(self, **endpoint_kwargs):
        return self.request('withdraw', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def new_order(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        payload = {'symbol': pair.format_for(self.name)}
        payload.update(endpoint_kwargs)
        return self.request('order/new', authenticate=True,
                            params=payload)

    @Bitfinex.check_version_compatibility
    def multiple_new_orders(self, *orders):
        raise NotImplementedError

    @Bitfinex.check_version_compatibility
    def cancel_multiple_orders(self, *order_ids):
        return self.request('order/cancel/multi', authenticate=True,
                            params={'order_ids': order_ids})

    @Bitfinex.check_version_compatibility
    def cancel_all_orders(self):
        return self.request('order/cancel/all', authenticate=True)

    @Bitfinex.check_version_compatibility
    def replace_order(self, **endpoint_kwargs):
        return self.request('order/cancel/replace', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def active_orders(self, *args, **kwargs):
        return self.request('orders', authenticate=True)

    @Bitfinex.check_version_compatibility
    def active_positions(self):
        return self.request('positions', authenticate=True)

    @Bitfinex.check_version_compatibility
    def claim_position(self, **endpoint_kwargs):
        return self.request('position/claim', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def balance_history(self, **endpoint_kwargs):
        return self.request('history', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def deposit_withdrawal_history(self, **endpoint_kwargs):
        return self.request('history/movement', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def past_trades(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        payload = {'symbol': pair.format_for(self.name)}
        payload.update(endpoint_kwargs)
        return self.request('mytrades', authenticate=True,
                            params=payload)

    @Bitfinex.check_version_compatibility
    def new_offer(self, **endpoint_kwargs):
        return self.request('offer/new', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def cancel_offer(self, **endpoint_kwargs):
        return self.request('offer/cancel', authenticate=False,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def offer_status(self, **endpoint_kwargs):
        return self.request('offer/status', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def active_credits(self, **endpoint_kwargs):
        return self.request('credits', authenticate=True,
                            params=endpoint_kwargs)

    def offers(self, **endpoint_kwargs):
        if self.api.version == 'v1':
            return self.request('offers', authenticate=True,
                                params=endpoint_kwargs)
        else:
            return self.request('auth/r/offers', authenticate=True,
                                params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def taken_funds(self, **endpoint_kwargs):
        return self.request('taken_funds', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def unused_taken_funds(self, **endpoint_kwargs):
        return self.request('unused_taken_funds', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def total_taken_funds(self, **endpoint_kwargs):
        return self.request('total_taken_funds', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def close_funding(self, **endpoint_kwargs):
        return self.request('funding/close', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def basket_manage(self, **endpoint_kwargs):
        return self.request('basket_manage', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def orders(self):
        return self.request('auth/r/orders', authenticate=True)

    @Bitfinex.check_version_compatibility
    def order_trades(self, pair, order_id, **endpoint_kwargs):
        return self.request('auth/r/order/%s:%s/trades' %
                            (pair.format_for(self.names), order_id),
                            authenticate=True, params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def positions(self):
        return self.request('auth/r/positions', authenticate=True)

    @Bitfinex.check_version_compatibility
    def offers(self):
        return self.request('auth/offers', authenticate=True)

    @Bitfinex.check_version_compatibility
    def performance(self):
        return self.request('auth/r/stats/perf:1D/hist', authenticate=True)

    @Bitfinex.check_version_compatibility
    def alert_list(self, **endpoint_kwargs):
        price = endpoint_kwargs.pop('type')
        return self.request('auth/r/alerts?type=%s' % price, authenticate=True)

    @Bitfinex.check_version_compatibility
    def alert_set(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        endpoint_kwargs['symbol'] = pair.format_for(self.name)
        return self.request('auth/w/alert/set', authenticate=True,
                            params=endpoint_kwargs)

    @Bitfinex.check_version_compatibility
    def alert_delete(self, pair, **endpoint_kwargs):
        self.is_supported(pair)
        symbol = endpoint_kwargs.pop('price')
        return self.request('auth/w/alert/price:%s:%s/del' %
                            (pair.format_for(self.name), price),
                            authenticate=True)

    @Bitfinex.check_version_compatibility
    def calc_available_balance(self, pair, **endpoint_kwargs)
        self.is_supported(pair)
        endpoint_kwargs['symbol'] = pair.format_for(self.name)
        return self.request('auth/calc/order/avail', authenticate=True,
                            params=endpoint_kwargs)

class Bitstamp(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Bitstamp, self).__init__('Bitstamp', BitstampREST(**APIKwargs))


class Bittrex(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Bittrex, self).__init__('Bittrex', BittrexREST(**APIKwargs))


class BTCE(RESTInterface):
    def __init__(self, **APIKwargs):
        super(BTCE, self).__init__('BTC-E', BTCEREST(**APIKwargs))


class Bter(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Bter, self).__init__('Bter', BterREST(**APIKwargs))


class CCEX(RESTInterface):
    def __init__(self, **APIKwargs):
        super(CCEX, self).__init__('C-CEX', CCEXREST(**APIKwargs))


class CoinCheck(RESTInterface):
    def __init__(self, **APIKwargs):
        super(CoincheckREST, self).__init__('CoinCheck',
                                            CoincheckREST(**APIKwargs))


class Cryptopia(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Cryptopia, self).__init__('Cryptopia', CryptopiaREST(**APIKwargs))


class HitBTC(RESTInterface):
    def __init__(self, **APIKwargs):
        super(HitBTC, self).__init__('HitBTC', HitBTCREST(**APIKwargs))


class Kraken(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Kraken, self).__init__('Kraken', KrakenREST(**APIKwargs))


class OKCoin(RESTInterface):
    def __init__(self, **APIKwargs):
        super(OKCoin, self).__init__('OKCoin', OKCoinREST(**APIKwargs))


class Poloniex(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Poloniex, self).__init__('Poloniex', PoloniexREST(**APIKwargs))


class QuadrigaCX(RESTInterface):
    def __init__(self, **APIKwargs):
        super(QuadrigaCX, self).__init__('QuadrigaCX',
                                         QuadrigaCXREST(**APIKwargs))


class TheRockTrading(RESTInterface):
    def __init__(self, **APIKwargs):
        super(TheRockTrading, self).__init__('The Rock Trading Ltd.',
                                             RockTradingREST(**APIKwargs))


class Vaultoro(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Vaultoro, self).__init__('Vaultoro', VaultoroREST(**APIKwargs))
