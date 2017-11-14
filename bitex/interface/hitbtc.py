# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.hitbtc import HitBTCREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class HitBTC(RESTInterface):
    def __init__(self, **api_kwargs):
        super(HitBTC, self).__init__('HitBTC', HitBTCREST(**api_kwargs))

    def _get_supported_pairs(self):
        r = self.request('symbols')
        return [entry['symbol'] for entry in r.json()['symbols']]

    # pylint: disable=arguments-differ
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
        return self.request('%s/trades', params=kwargs)

    # Private Endpoints
    # pylint: disable=unused-argument
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

    # pylint: disable=arguments-differ
    def cancel_order(self, *order_ids, cancel_all=False, **kwargs):
        if cancel_all:
            return self.request('cancel_orders', authenticate=True, verb='POST',
                                params=kwargs)
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
