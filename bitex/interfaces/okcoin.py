"""
https://www.okcoin.com/about/rest_api.do
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import OKCoinREST
from bitex.utils import return_json

# Init Logging Facilities
log = logging.getLogger(__name__)


class OKCoin(OKCoinREST):
    def __init__(self, key='', secret='', key_file=''):
        super(OKCoin, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """
    @return_json(None)
    def ticker(self, pair):
        return self.public_query('ticker.do', params={'pair': pair})

    @return_json(None)
    def order_book(self, pair):
        return self.public_query('depth.do', params={'pair': pair})

    @return_json(None)
    def trades(self, pair):
        return self.public_query('trades.do', params={'pair': pair})

    @return_json(None)
    def bid(self, pair, price, amount, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def ask(self, pair, price, amount, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def cancel_order(self, order_id, all=False, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def order(self, order_id, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def balance(self, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def withdraw(self, _type, source_wallet, amount, tar_addr, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def deposit_address(self, **kwargs):
        raise NotImplementedError()

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def ohlc(self, pair):
        return self.public_query('kline.do', params={'pair': pair})

    @return_json(None)
    def future_ticker(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_ticker.do', params=q)

    @return_json(None)
    def future_order_book(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_order_book.do', params=q)

    @return_json(None)
    def future_trades(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_trades.do', params=q)

    @return_json(None)
    def future_index(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_index.do', params=q)

    @return_json(None)
    def usd_cny_rate(self):
        return self.public_query('exchange_rate.do', params=q)

    @return_json(None)
    def future_estimate(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_estimated_price.do', params=q)

    @return_json(None)
    def future_ohlc(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_kline.do', params=q)

    @return_json(None)
    def future_holds(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_hold_amount.do', params=q)

    @return_json(None)
    def future_limit_price(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('future_price_limit.do', params=q)

    @return_json(None)
    def otc_order_book(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('otcs.do', params=q)