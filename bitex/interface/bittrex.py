"""Bitstamp Interface class."""
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.bittrex import BittrexREST

from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bittrex(RESTInterface):
    """Bittrex REST API Interface Class."""

    def __init__(self, **api_kwargs):
        super(Bittrex, self).__init__('Bittrex', BittrexREST(**api_kwargs))

    # pylint: disable=arguments-differ
    def request(self, endpoint, authenticate=False, **req_kwargs):
        return super(Bittrex, self).request('GET', endpoint, authenticate, **req_kwargs)

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
        return self.request('market/selllimit', params=payload, authenticate=True)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        payload = {'market': pair, 'quantity': size, 'rate': price}
        payload.update(kwargs)
        return self.request('market/buylimit', params=payload, authenticate=True)

    def order_status(self, order_id, *args, **kwargs):
        payload = {'uuid': order_id}
        payload.update(kwargs)
        return self.request('account/getorder', params=payload, authenticate=True)

    def open_orders(self, *args, **kwargs):
        return self.request('market/getopenorders', params=kwargs, authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for uuid in order_ids:
            payload.update({'uuid': uuid})
            r = self.request('market/cancel', params=payload, authenticate=True)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, currency=None, *args, **kwargs):  # pylint: disable=arguments-differ
        if currency:
            payload = {'currency': currency}
            payload.update(kwargs)
            return self.request('account/getbalance', params=payload, authenticate=True)
        payload = kwargs
        return self.request('account/getbalances', params=payload, authenticate=True)

    ###########################
    # Exchange Specific Methods
    ###########################

    def deposit_address(self, currency, **kwargs):
        """Return the deposit address for given currency."""
        payload = {'currency': currency}
        payload.update(kwargs)
        return self.request('account/getdepositaddress', params=payload, authenticate=True)

    def withdraw(self, **kwargs):
        """Issue a withdrawal."""
        return self.request('account/withdraw', params=kwargs)

    def trade_history(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Return the account's trade history."""
        return self.request('account/getorderhistory', params=kwargs)

    def withdrawal_history(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Return the account's withdrawal history."""
        return self.request('account/getwithdrawalhistory', params=kwargs)

    def deposit_history(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Return the account's deposit history."""
        return self.request('account/getdeposithistory', params=kwargs)

    def pairs(self, **kwargs):
        """Return the available pairs."""
        return self.request('public/getmarkets', params=kwargs)

    def currencies(self, **kwargs):
        """Return traded currencies."""
        return self.request('public/getcurrencies', params=kwargs)

    def simple_ticker(self, **kwargs):
        """Return a simple ticker for a given pair."""
        return self.request('public/getticker', params=kwargs)
