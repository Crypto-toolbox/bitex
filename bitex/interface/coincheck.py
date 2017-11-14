"""CoinCheck Interface class."""
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.coincheck import CoincheckREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class CoinCheck(RESTInterface):
    """Interface Class for the Coincheck.com REST API.

    Documentation:
        https://coincheck.com/documents/exchange/api

    The API documentation appears to be not up-to-date, or the endpoints
    not updated to support the various new pairs at the exchange.
    """

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(CoinCheck, self).__init__('CoinCheck',
                                        CoincheckREST(**api_kwargs))

    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        return ['btc-jpy']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        return self.request('GET', 'ticker', params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        return self.request('GET', 'order_books', params=kwargs)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        return self.request('GET', 'trades', params=kwargs)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        """Place an order with the given parameters."""
        payload = {'rate': price, 'amount': size, 'pair': pair,
                   'order_type': side}
        payload.update(kwargs)
        return self.request('POST', 'exchange/orders', params=payload,
                            authenticate=True)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask orders."""
        if 'order_type' in kwargs:
            if (kwargs['order_type'] not in
                    ('sell', 'market_sell', 'leverage_sell', 'close_short')):
                raise ValueError("order_type not supported by this function!")
        return self._place_order(pair, price, size, 'sell', **kwargs)

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        if 'order_type' in kwargs:
            if (kwargs['order_type'] not in
                    ('buy', 'market_buy', 'leverage_buy', 'close_long')):
                raise ValueError("order_type not supported by this function!")
        return self._place_order(pair, price, size, 'sell', **kwargs)

    def order_status(self, order_id, *args, **kwargs):
        """Return the status of the order with the given ID.

        Currently NOT IMPLEMENTED.
        """
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        """Return a list of all open orders."""
        return self.request('GET', 'exchange/orders/open', params=kwargs,
                            authenticate=True)

    def cancel_order(self, *order_ids, **kwargs):
        """Cancel order(s) with the given ID(s)."""
        result = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'order_id': oid})
            r = self.request('DELETE', 'exchange/orders/' + oid,
                             params=payload, authenticate=True)
            result.append(r)
        return r if len(r) > 1 else r[0]

    def wallet(self, *args, **kwargs):
        """Return the account's wallet."""
        return self.request('GET', 'accounts/balance', params=kwargs,
                            authenticate=True)
