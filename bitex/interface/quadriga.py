# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.quadriga import QuadrigaCXREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


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

