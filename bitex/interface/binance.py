"""Binance Interface class."""
# Import Built-Ins
import logging

# Import Third-party
import requests

# Import Homebrew
from bitex.api.REST.binance import BinanceREST
from bitex.interface.rest import RESTInterface
from bitex.utils import format_with, check_and_format_pair
from bitex.formatters import BinanceFormattedResponse

# Init Logging Facilities
log = logging.getLogger(__name__)


class Binance(RESTInterface):
    """Binance Interface class.

    Includes standardized methods, as well as all other Endpoints
    available on their REST API.
    """

    # pylint: disable=arguments-differ
    def __init__(self, **api_kwargs):
        """Initialize class instance."""
        super(Binance, self).__init__('Binance', BinanceREST(**api_kwargs))

    def request(self, verb, endpoint, authenticate=False, **req_kwargs):
        """Preprocess request to API."""
        return super(Binance, self).request(verb, endpoint, authenticate=authenticate, **req_kwargs)

    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        r = self.exchange_information().json()
        pairs = [entry['symbol'] for entry in r['symbols']]
        return pairs

    @check_and_format_pair
    @format_with(BinanceFormattedResponse)
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        kwargs.update({'symbol': pair})
        return self.request('GET', 'api/v1/ticker/24hr', params=kwargs)

    @check_and_format_pair
    @format_with(BinanceFormattedResponse)
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        kwargs.update({'symbol': pair})
        return self.request('GET', 'api/v1/depth', params=kwargs)

    @check_and_format_pair
    @format_with(BinanceFormattedResponse)
    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        kwargs.update({'symbol': pair})
        return self.request('GET', 'api/v1/trades', params=kwargs)

    # Private Endpoints
    # pylint: disable=unused-argument
    def _place_order(self, pair, price, size, side, *args, **kwargs):
        kwargs.update({'symbol': pair,
                       'side': side,
                       'type': "LIMIT_MAKER",
                       'price': price,
                       'quantity': size})
        return self.request('POST', 'api/v3/order', authenticate=True, params=kwargs)

    @check_and_format_pair
    @format_with(BinanceFormattedResponse)
    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask order."""
        return self._place_order(pair, price, size, "SELL", *args, **kwargs)

    @check_and_format_pair
    @format_with(BinanceFormattedResponse)
    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        return self._place_order(pair, price, size, "BUY", *args, **kwargs)

    @format_with(BinanceFormattedResponse)
    def order_status(self, order_id, pair, *args, **kwargs):
        """Return the status of an order with the given id."""
        kwargs.update({'symbol': pair, 'orderId': order_id})
        return self.request('GET', 'api/v3/order', authenticate=True, params=kwargs)

    @format_with(BinanceFormattedResponse)
    def open_orders(self, *args, **kwargs):
        """Return all open orders."""
        return self.request('GET', 'api/v3/openOrders', authenticate=True, params=kwargs)

    @format_with(BinanceFormattedResponse)
    def cancel_order(self, *order_ids, pair, **kwargs):
        """Cancel the order(s) with the given id(s)."""
        results = []
        for order_id in order_ids:
            kwargs.update({'symbol': pair, 'orderId': order_id})
            r = self.request('DELETE', 'api/v3/order', authenticate=True, params=kwargs)
            results.append(r)
        return results if len(results) > 1 else results[0]

    @format_with(BinanceFormattedResponse)
    def wallet(self, *args, **kwargs):
        """Return the wallet of this account and also the current account information."""
        return self.request('GET', 'api/v3/account', authenticate=True)

    ###########################
    # Exchange Specific Methods
    ###########################

    def exchange_information(self):
        """Return current exchange trading rules and symbol information."""
        return self.request('GET', 'api/v1/exchangeInfo')

    def all_orders(self, currency, **kwargs):
        """Return all account orders; active, canceled, or filled."""
        if currency:
            kwargs.update({'symbol': currency})
        return self.request('GET', 'api/v3/allOrders', authenticate=True, params=kwargs)

    def trade_history(self, pair, **kwargs):
        """Return past trades of the account."""
        if pair:
            try:
                pair = pair.format_for(self.name).upper()
            except AttributeError:
                pass
                kwargs.update({'symbol': pair})
        return self.request('GET', 'api/v3/myTrades', authenticate=True, params=kwargs)

    def withdraw(self, currency, amount, address, address_tag=None, **kwargs):
        """Withdraw currency from the account."""
        kwargs.update({'asset': currency, 'amount': amount, 'address': address})
        if address_tag:
            kwargs.update({'addressTag': address_tag})
        # force a name for the withdrawal if it's not set
        # (according to the docs it's optional, but in reality it's mandatory)
        if 'name' not in kwargs:
            kwargs['name'] = kwargs['asset']
        return self.request('POST', 'wapi/v3/withdraw.html', authenticate=True, params=kwargs)

    def deposit_history(self, currency=None, **kwargs):
        """Return the deposit history of the account."""
        if currency:
            kwargs.update({'asset': currency})
        return self.request('GET', 'wapi/v3/depositHistory.html', authenticate=True, params=kwargs)

    def withdraw_history(self, currency=None, **kwargs):
        """Return the withdrawal history of the account."""
        if currency:
            kwargs.update({'asset': currency})
        return self.request('GET', 'wapi/v3/withdrawHistory.html', authenticate=True, params=kwargs)

    def deposit_address(self, currency, **kwargs):
        """Return the deposit address for the given currency."""
        kwargs.update({'asset': currency})
        return self.request('GET', 'wapi/v3/depositAddress.html', authenticate=True, params=kwargs)

    def withdraw_fee(self, currency, **kwargs):
        """Return the withdrawal fee for the given currency."""
        kwargs.update({'asset': currency})
        return self.request('GET', 'wapi/v3/withdrawFee.html', authenticate=True, params=kwargs)
