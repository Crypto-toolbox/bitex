# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.poloniex import PoloniexREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class Poloniex(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Poloniex, self).__init__('Poloniex', PoloniexREST(**APIKwargs))

    # pylint: disable=arguments-differ
    def request(self, endpoint, authenticate=False, **req_kwargs):
        if 'params' in req_kwargs:
            req_kwargs['params'].update({'command': endpoint})
        else:
            req_kwargs['params'] = {'command': endpoint}
        if authenticate:
            return super(Poloniex, self).request('POST', endpoint, authenticate,
                                                 **req_kwargs)
        return super(Poloniex, self).request('GET', 'public', authenticate,
                                             **req_kwargs)

    def _get_supported_pairs(self):
        return ['BTC_ETH']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        return self.request('returnTicker', params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        payload = {'currencyPair': pair}
        payload.update(kwargs)
        return self.request('returnOrderBook', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        payload = {'currencyPair': pair}
        payload.update(kwargs)
        return self.request('returnTradeHistory', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        payload = {'currencyPair': pair, 'rate': price, 'amount': size}
        payload.update(kwargs)
        if side == 'bid':
            return self.request('buy', authenticate=True, params=payload)
        return self.request('sell', authenticate=True, params=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        payload = {'orderNumber': order_id}
        payload.update(kwargs)
        return self.request('returnOrderTrades', authenticate=True, params=payload)

    def open_orders(self, *args, **kwargs):
        payload = {'currencyPair': 'all'}
        payload.update(kwargs)
        return self.request('returnOpenOrders', authenticate=True, params=payload)

    def cancel_order(self, *order_ids, **kwargs):
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'orderNumber', oid})
            r = self.request('cancelOrder', authenticate=True, params=oid)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        return self.request('returnTradableBalances', authenticate=True, params=kwargs)
