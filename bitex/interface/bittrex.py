"""Bitstamp Interface class."""
# Import Built-Ins
import logging

# Import Third-party
import requests

# Import Homebrew
from bitex.api.REST.bittrex import BittrexREST

from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair, format_with
from bitex.formatters import BittrexFormattedResponse

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bittrex(RESTInterface):
    """Bittrex REST API Interface Class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(Bittrex, self).__init__('Bittrex', BittrexREST(**api_kwargs))

    # pylint: disable=arguments-differ
    def request(self, endpoint, authenticate=False, **req_kwargs):
        """Generate a request to the API."""
        return super(Bittrex, self).request('GET', endpoint, authenticate=authenticate,
                                            **req_kwargs)

    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        r = requests.request('GET', 'https://bittrex.com/api/v1.1/public/getmarkets').json()
        pairs = [item['MarketName'] for item in r['result']]
        return pairs

    ###############
    # Basic Methods
    ###############
    @format_with(BittrexFormattedResponse)
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        kwargs.update({'market': pair})
        return self.request('public/getmarketsummary', params=kwargs)

    @check_and_format_pair
    @format_with(BittrexFormattedResponse)
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        kwargs.update({'market': pair, 'type': 'both'})
        return self.request('public/getorderbook', params=kwargs)

    @check_and_format_pair
    @format_with(BittrexFormattedResponse)
    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        kwargs.update({'market': pair})
        return self.request('public/getmarkethistory', params=kwargs)

    # Private Endpoints
    @check_and_format_pair
    @format_with(BittrexFormattedResponse)
    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask order."""
        kwargs.update({'market': pair, 'quantity': size, 'rate': price})
        return self.request('market/selllimit', params=kwargs, authenticate=True)

    @check_and_format_pair
    @format_with(BittrexFormattedResponse)
    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        kwargs.update({'market': pair, 'quantity': size, 'rate': price})
        return self.request('market/buylimit', params=kwargs, authenticate=True)

    @format_with(BittrexFormattedResponse)
    def order_status(self, order_id, *args, **kwargs):
        """Return order status of order with given id."""
        kwargs.update({'uuid': order_id})
        return self.request('account/getorder', params=kwargs, authenticate=True)

    @format_with(BittrexFormattedResponse)
    def open_orders(self, *args, **kwargs):
        """Return all open orders."""
        return self.request('market/getopenorders', params=kwargs, authenticate=True)

    @format_with(BittrexFormattedResponse)
    def cancel_order(self, *order_ids, **kwargs):
        """Cancel order(s) with given ID(s)."""
        results = []
        for uuid in order_ids:
            kwargs.update({'uuid': uuid})
            r = self.request('market/cancel', params=kwargs, authenticate=True)
            results.append(r)
        return results if len(results) > 1 else results[0]

    @format_with(BittrexFormattedResponse)
    # pylint: disable=arguments-differ
    def wallet(self, *args, currency=None, **kwargs):
        """Return the account wallet."""
        endpoint = 'account/getbalances'
        if currency:
            endpoint = 'account/getbalance'
            kwargs.update({'currency': currency})
        return self.request(endpoint, params=kwargs, authenticate=True)

    ###########################
    # Exchange Specific Methods
    ###########################

    def deposit_address(self, currency, **kwargs):
        """Return the deposit address for given currency."""
        kwargs.update({'currency': currency})
        return self.request('account/getdepositaddress', params=kwargs, authenticate=True)

    def withdraw(self, **kwargs):
        """Issue a withdrawal."""
        return self.request('account/withdraw', params=kwargs, authenticate=True)

    def trade_history(self, pair=None, **kwargs):
        """Return the account's trade history."""
        if pair:
            try:
                pair = pair.format_for(self.name)
            except AttributeError:
                pair = pair
            kwargs.update({'market': pair})
        return self.request('account/getorderhistory', params=kwargs, authenticate=True)

    def withdrawal_history(self, currency=None, **kwargs):
        """Return the account's withdrawal history."""
        if currency:
            kwargs.update({'currency': currency})
        return self.request('account/getwithdrawalhistory', params=kwargs, authenticate=True)

    def deposit_history(self, currency=None, **kwargs):
        """Return the account's deposit history."""
        if currency:
            kwargs.update({'currency': currency})
        return self.request('account/getdeposithistory', params=kwargs, authenticate=True)

    def pairs(self, **kwargs):
        """Return the available pairs."""
        return self.request('public/getmarkets', params=kwargs)

    def currencies(self, **kwargs):
        """Return traded currencies."""
        return self.request('public/getcurrencies', params=kwargs)

    def simple_ticker(self, **kwargs):
        """Return a simple ticker for a given pair."""
        return self.request('public/getticker', params=kwargs)
