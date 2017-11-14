"""Bitstamp Interface class."""
# pylint: disable=arguments-differ
# Import Built-Ins
import logging

# Import Homebrew
from bitex.exceptions import UnsupportedPairError
from bitex.api.REST.bitstamp import BitstampREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitstamp(RESTInterface):
    """Bitstamp REST API Interface Class.

    Since Bitstamp doesn't make an explicit differentiation between api versions,
    we do not use a version checker for this interface.
    """
    def __init__(self, **api_kwargs):
        super(Bitstamp, self).__init__('Bitstamp', BitstampREST(**api_kwargs))

    def _get_supported_pairs(self):
        return ['btceur', 'btcusd', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc',
                'ltcusd', 'ltceur', 'ltcbtc']

    def request(self, endpoint, authenticate=False, **kwargs):
        verb = 'POST' if authenticate else 'GET'
        return super(Bitstamp, self).request(verb, endpoint, authenticate=authenticate, **kwargs)

    ###############
    # Basic Methods
    ###############

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('ticker/%s/' % pair, params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        return self.request('order_book/%s/' % pair, params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        return self.request('transactions/%s/' % pair, params=kwargs)

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, market=False, **kwargs):
        return self._place_order(pair, price, size, 'buy', market=market, **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, market=False, **kwargs):
        return self._place_order(pair, price, size, 'buy', market=market, **kwargs)

    def _place_order(self, pair, size, price, side, market=None, **kwargs):
        payload = {'amount': size, 'price': price}
        payload.update(kwargs)
        if market:
            return self.request('%s/market/%s/' % (side, pair), authenticate=True, data=payload)
        return self.request('%s/%s/' % (side, pair), authenticate=True, data=payload)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'id': order_id}
        payload.update(kwargs)
        return self.request('api/order_status/', authenticate=True, data=payload)

    def open_orders(self, *args, pair=None, **kwargs):
        if pair:
            return self.request('open_orders/%s/' % pair, authenticate=True, data=kwargs)
        return self.request('open_orders/all/', authenticate=True, data=kwargs)

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
            return self.request('balance/%s/' % pair, authenticate=True, data=kwargs)
        return self.request('balance/', authenticate=True, data=kwargs)

    ###########################
    # Exchange Specific Methods
    ###########################

    @check_and_format_pair
    def hourly_ticker(self, pair, **kwargs):
        if pair:
            return self.request('ticker_hour/%s/' % pair, params=kwargs)
        return self.request('api/ticker_hour/')

    def eur_usd_conversion_rate(self, **kwargs):
        return self.request('api/eur_usd/', params=kwargs)

    @check_and_format_pair
    def user_transactions(self, pair, **kwargs):
        if pair:
            return self.request('user_transactions/%s/' % pair, authenticate=True, data=kwargs)
        return self.request('api/user_transactions/', authenticate=True, data=kwargs)

    def cancel_all_orders(self, **kwargs):
        return self.request('api/cancel_all_orders/', authenticate=True, data=kwargs)

    def withdrawal_request(self, **kwargs):
        return self.request('api/withdrawal_request', authenticate=True, data=kwargs)

    def withdraw(self, currency, **kwargs):  # pylint: disable=unused-argument
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
