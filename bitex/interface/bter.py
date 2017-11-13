# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.bter import BterREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


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

