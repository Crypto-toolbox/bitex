"""Bitstamp Interface class."""
# pylint: disable=arguments-differ
# Import Built-Ins
import logging

import requests

# Import Homebrew
from bitex.api.REST.bitstamp import BitstampREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair, format_with
from bitex.formatters import BitstampFormattedResponse


# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitstamp(RESTInterface):
    """Bitstamp REST API Interface Class.

    Since Bitstamp doesn't make an explicit differentiation between api versions,
    we do not use a version checker for this interface.
    """

    def __init__(self, **api_kwargs):
        """Initialize the Interface class instance."""
        super(Bitstamp, self).__init__('Bitstamp', BitstampREST(**api_kwargs))

    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        resp = requests.request('GET', 'https://www.bitstamp.net/api/v2/trading-pairs-info/')
        return [pair["name"].replace("/", "").lower() for pair in resp.json()]

    def request(self, endpoint, authenticate=False, **kwargs):
        """Generate a request to the API."""
        verb = 'POST' if authenticate else 'GET'
        return super(Bitstamp, self).request(verb, endpoint, authenticate=authenticate, **kwargs)

    ###############
    # Basic Methods
    ###############

    # Public Endpoints

    @check_and_format_pair
    @format_with(BitstampFormattedResponse)
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        return self.request('ticker/%s/' % pair, params=kwargs)

    @check_and_format_pair
    @format_with(BitstampFormattedResponse)
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        return self.request('order_book/%s/' % pair, params=kwargs)

    @check_and_format_pair
    @format_with(BitstampFormattedResponse)
    def trades(self, pair, *args, **kwargs):
        """Return trades for the given pair."""
        return self.request('transactions/%s/' % pair, params=kwargs)

    # Private Endpoints
    @check_and_format_pair
    @format_with(BitstampFormattedResponse)
    def ask(self, pair, price, size, *args, market=False, **kwargs):
        """Place an ask order."""
        return self._place_order(pair, price, size, 'sell', market=market, **kwargs)

    @check_and_format_pair
    @format_with(BitstampFormattedResponse)
    def bid(self, pair, price, size, *args, market=False, **kwargs):
        """Place a bid order."""
        return self._place_order(pair, price, size, 'buy', market=market, **kwargs)

    def _place_order(self, pair, price, size, side, market=None, **kwargs):
        """Place an order with the given parameters."""
        kwargs.update({'amount': size, 'price': price})
        suffix = 'market/' if market else ''
        return self.request('%s/%s%s/' % (side, suffix, pair), authenticate=True, params=kwargs)

    @format_with(BitstampFormattedResponse)
    def order_status(self, order_id, *args, **kwargs):
        """Return the order status for the given order's ID."""
        kwargs.update({'id': order_id})
        return self.request('api/order_status/', authenticate=True, params=kwargs)

    @format_with(BitstampFormattedResponse)
    def open_orders(self, *args, pair=None, **kwargs):
        """Return all open orders."""
        suffix = pair or 'all'
        return self.request('open_orders/%s/' % suffix, authenticate=True, params=kwargs)

    @format_with(BitstampFormattedResponse)
    def cancel_order(self, *order_ids, **kwargs):
        """Cancel existing order(s) with the given id(s)."""
        results = []
        for oid in order_ids:
            kwargs.update({'id': oid})
            r = self.request('cancel_order/', authenticate=True, params=kwargs)
            results.append(r)
        return results if len(results) > 1 else results[0]

    @format_with(BitstampFormattedResponse)
    def wallet(self, *args, pair=None, **kwargs):
        """Return account's wallet."""
        endpoint = 'balance/'
        if pair:
            try:
                pair = pair.format_for(self.name).lower()
            except AttributeError:
                pass
            endpoint += pair + '/'
        return self.request(endpoint, authenticate=True, params=kwargs)

    ###########################
    # Exchange Specific Methods
    ###########################

    @check_and_format_pair
    def hourly_ticker(self, pair):
        """Return the hourly ticker for the given pair."""
        return self.request('ticker_hour/' + pair)

    def eur_usd_conversion_rate(self):
        """Return EUR/USD conversion rate."""
        return self.request('api/eur_usd/')

    def user_transactions(self, pair=None, **kwargs):
        """Return user transactions."""
        endpoint = 'user_transactions/'
        if pair:
            try:
                pair = pair.format_for(self.name).lower()
            except AttributeError:
                pass
            endpoint += pair + '/'
        return self.request(endpoint, authenticate=True, params=kwargs)

    def cancel_all_orders(self):
        """Cancel all orders."""
        return self.request('cancel_all_orders/', authenticate=True)

    def withdraw(self, currency, **kwargs):
        """Withdraw currency from the account."""
        currency = currency.lower()
        if currency == 'btc':
            endpoint = 'api/bitcoin_withdrawal/'
        elif currency == 'xrp':
            endpoint = 'api/ripple_withdrawal/'
        else:
            endpoint = '%s_withdrawal/' % currency
        return self.request(endpoint, authenticate=True, params=kwargs)

    def withdrawal_requests(self, **kwargs):
        """Returns user withdrawal requests."""
        return self.request('withdrawal-requests/', authenticate=True, params=kwargs)

    def deposit_address(self, currency):
        """Return the currency's deposit address."""
        currency = currency.lower()
        if currency == 'btc':
            endpoint = 'api/bitcoin_deposit_address/'
        elif currency == 'xrp':
            endpoint = 'api/ripple_address/'
        else:
            endpoint = '%s_address/' % currency
        return self.request(endpoint, authenticate=True)

    def unconfirmed_bitcoin_deposits(self):
        """Return all unconfirmed bitcoin deposits."""
        return self.request('api/unconfirmed_btc/', authenticate=True)

    def transfer_sub_to_main(self, **kwargs):
        """Transfer currency from sub account to main."""
        return self.request('transfer-to-main/', authenticate=True, params=kwargs)

    def transfer_main_to_sub(self, **kwargs):
        """Transfer currency from main account to sub account."""
        return self.request('transfer-from-main/', authenticate=True, params=kwargs)

    def open_bank_withdrawal(self, **kwargs):
        """Issue a bank withdrawal."""
        return self.request('withdrawal/open/', authenticate=True, params=kwargs)

    def bank_withdrawal_status(self, **kwargs):
        """Query status of a bank withdrawal."""
        return self.request('withdrawal/status/', authenticate=True, params=kwargs)

    def cancel_bank_withdrawal(self, **kwargs):
        """Cancel a bank withdrawal."""
        return self.request('withdrawal/cancel/', authenticate=True, params=kwargs)

    def liquidate(self, **kwargs):
        """Liquidate all assets."""
        return self.request('liquidation_address/new/', authenticate=True, params=kwargs)

    def liquidation_info(self, **kwargs):
        """Return liquidity information."""
        return self.request('liquidation_address/info/', authenticate=True, params=kwargs)
