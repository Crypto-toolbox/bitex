"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.kraken import API
from bitex.http.client import Client


log = logging.getLogger(__name__)


class KrakenHTTP(Client):
    def __init__(self, key='', secret='', key_file=''):
        api = API(key, secret)
        if key_file:
            api.load_key(key_file)
        super(KrakenHTTP, self).__init__(api, 'Kraken')


    def order_book(self, pair, count=0):
        """
        Returns orderbook for passed asset pair.
        :param pair:
        :param count:
        :return:
        """
        q = {'pair': pair}
        if count:
            q['count'] = count

        resp = self.query('public/Depth', params=q)

        return resp, pair

    def server_time(self):
        """
        Returns the Kraken server time in unix
        :return: list
        """
        response = self._api.query_public('public/Time')
        return response

    def assets(self, assets='all', info='info', aclass='currency'):
        """
        Returns a list of Assets available at Kraken.

        sent|received|asset|type|value

        :param assets: Assets to get info on.
        :type assets: str, list, tuple
        :param info: info to retrieve
        :type info: str
        :param aclass: asset class to query for.
        :type aclass: str
        :return: list
        """
        q = {'info': info, 'aclass': aclass}
        if assets != 'all':
            if isinstance(assets, list):
                q['assets'] = ','.join(assets)
            elif isinstance(assets, str):
                q['assets'] = assets

        response = self._api.query_public('public/Assets', params=q)
        return response

    def asset_pairs(self, pairs='all', info='info'):
        """
        Returns a listing of all tradable asset pairs, plus additional information.
        :param pairs: Asset pairs to get ticker for
        :type pairs: str, list, tuple
        :param info: info to retrieve; one of 'info', 'leverage', 'fees', 'margin'.
        :return:
        """
        q = {'info': info}
        if pairs != 'all':
            if isinstance(pairs, list):
                q['assets'] = ','.join(pairs)
            elif isinstance(pairs, str):
                q['assets'] = pairs

        response = self._api.query_public('public/AssetPairs', params=q)

        return response

    def ticker(self, pairs):
        """
        Returns Ticker information for passed asset pairs.
        :param pairs:
        :return:
        """
        if isinstance(pairs, (list, tuple)):
            pairs = ','.join(pairs)

        q = {'pair': pairs}
        response = self._api.query('public/Ticker', params=q)
        return response

    def ohlc(self, pair, interval=1, since=None):
        """
        Returns OHLC data for passed asset pair.
        :param pair:
        :param interval:
        :param since:
        :return:
        """
        q = {'pair': pair, 'interval': interval}
        if since is not None:
            q['since'] = since

        response = self._api.query_public('public/OHLC', params=q)
        return response

    def trades(self, pair, since=None):
        """
        Returns trades for passed asset pair.
        :param pair:
        :param since:
        :return:
        """
        q = {'pair': pair}
        if since is not None:
            q['since'] = None

        response = self._api.query_public('public/Trades', params=q)
        return response

    def spread(self, pair, since=None):
        """
        Returns spread data for passed asset pair.
        :param pair:
        :param since:
        :return:
        """
        q = {'pair': pair}
        if since is not None:
            q['since'] = None

        response = self._api.query_public('public/Spread', params=q)
        return response

    def balance(self, asset='ZUSD', aclass=None):
        """
        Returns user's account balance.
        :param asset: Base asset used to determine balance (default ZUSD)
        :param aclass: asset class - default is currency.
        :return: dict
        """
        q = {'asset': asset}
        if aclass is not None:
            q['aclass'] = aclass

        response = self._api.query('private/TradeBalance', params=q, post=True,
                                   authenticate=True)
        return response

    def open_orders(self, trades=False, userref=None):
        """
        Returns user account's open orders.
        :param trades:
        :param userref:
        :return:
        """
        q = {}
        if trades:
            q['trades'] = trades

        if userref is not None:
            q['userref'] = userref

        response = self._api.query_private('private/OpenOrders', params=q)
        return response

    def closed_orders(self, ofs, trades=False, userref=None, start=None, end=None,
                      closetime='both'):
        """
        Returns user account's closed orders.
        :param ofs:
        :param trades:
        :param userref:
        :param start:
        :param end:
        :param closetime:
        :return:
        """
        q = {'ofs': ofs}
        q['closetime'] = closetime
        if trades:
            q['trades'] = trades

        if userref is not None:
            q['userref'] = userref

        if start is not None:
            q['start'] = start

        if end is not None:
            q['end'] = end

        response = self._api.query_private('private/ClosedOrders', params=q)
        return response

    def query_orders(self, trades=False, userref=None, txid=None):
        """
        Returns information from user's account about orders.
        :param trades:
        :param userref:
        :param txid:
        :return:
        """
        q = {'trades': trades}
        if userref is not None:
            q['userref'] = userref

        if txid is not None:
            q['txid'] = txid

        response = self._api.query_private('private/QueryOrders', params=q)
        return response

    def trade_history(self, ofs, trade_type='all', trades=False, start=None, end=None):
        """
        Returns the user account's trade history.
        :param ofs:
        :param type_:
        :param trades:
        :param start:
        :param end:
        :return:
        """
        q = {'ofs': ofs, 'trades': trades}

        if trade_type in ('all', 'any position', 'closed position', 'open position',
                     'no position'):
            q['type'] = trade_type

        if start is not None:
            q['start'] = start

        if end is not None:
            q['end'] = end

        response = self._api.query_private('private/TradesHistory', params=q)
        return response

    def trade_info(self, txid, trades=False):
        """
        Returns user account's trade information.
        :param txid:
        :param trades:
        :return:
        """
        q = {'trades': trades, 'txid': txid}

        response = self._api.query_private('private/QueryTrades', params=q)
        return response

    def open_positions(self, txid, docalcs=False):
        """
        Returns user account's open positions.
        :param txid:
        :param docalcs:
        :return:
        """
        q = {'txid': self.__validate_txid(txid), 'docalcs': docalcs}

        response = self._api.query_private('private/OpenPositions', params=q)
        return response

    def ledgers(self, ofs, aclass='currency', asset='all', ledger_type='all',
                start=None, end=None):
        """
        Returns user account's ledgers.
        :param ofs:
        :param aclass:
        :param asset:
        :param type_:
        :param start:
        :param end:
        :return:
        """
        q = {'ofs': ofs, 'aclass': aclass, 'type': ledger_type}

        if isinstance(asset, (tuple, list)):
            q['asset'] = ','.join(asset)
        else:
            q['asset'] = asset

        if start is not None:
            q['start'] = start

        if end is not None:
            q['end'] = end

        response = self._api.query_private('private/Ledgers', params=q)
        return response

    def query_ledger(self, ids):
        """
        Return information about passed id from user account's ledger
        :param ids:
        :return:
        """
        q = {'id': self.__validate_txid(id)}

        response = self._api.query_private('private/QueryLedgers', params=q)
        return response

    def trade_volume(self, pairs=None, fee_info=None):
        """
        Return user account's trade volume.
        :param pairs:
        :param fee_info:
        :return:
        """
        q = {}
        if pairs is not None:
            if isinstance(pairs, (tuple, list)):
                q['pair'] = ','.join(pairs)
            elif isinstance(pairs, str):
                q['pair'] = pairs
            else:
                raise ValueError("Invalid type for pairs parameter!")

        if fee_info is not None:
            q['fee-info'] = fee_info

        response = self._api.query_private('private/TradeVolume', params=q)
        return response

    def add_order(self, pair, ordertype, volume, price=None, price2=None,
                  leverage=None, oflags=None, starttm=None, expiretm=None,
                  userref=None, validate=None, **close_kwargs):
        """
        Add an order for passed pair of passed ordertype and volume.
        :param pair:
        :param ordertype:
        :param volume:
        :param price:
        :param price2:
        :param leverage:
        :param oflags:
        :param starttm:
        :param expiretm:
        :param userref:
        :param validate:
        :param close_ordertype:
        :param close_price:
        :param close_price2:
        :return:
        """
        q = {'pair': pair, 'ordertype': ordertype, 'volume': volume}

        if ordertype not in ('market', 'settle-position') and price is None:
            raise ValueError("Must supply price parameter for market orders!")
        else:
            q['price'] = price

        if (ordertype in ('stop-loss-profit', 'stop-loss-profit-limit',
                            'stop-loss-limit', 'take-profit-limit',
                            'trailing-stop-limit', 'stop-loss-and-limit')
            and price2 is None):
            raise ValueError("Must supply price2 parameter for market orders!")
        else:
            q['price2'] = price2

        response = self._api.query_private('private/AddOrder', params=q)
        return response

    def cancel_order(self, txid):
        """
        Cancel an order by passed txid.
        :param txid:
        :return:
        """
        q = {'txid': txid}

        response = self._api.query_private('CancelOrder', params=q)
        return response

    def deposit_method(self, asset, aclass='currency'):
        """
        Query user account's deposit mehtod for passed asset.
        :param asset:
        :param aclass:
        :return:
        """
        q = {'asset': asset, 'aclass': aclass}

        response = self._api.query_private('private/DepositMethods', params=q)
        return response

    def deposit_addresses(self, asset, method, new=False, aclass='currency'):
        """
        Return user account's deposit address for passed asset and method.
        :param asset:
        :param method:
        :param new:
        :param aclass:
        :return:
        """
        q = {'asset': asset, 'method': method, 'new': new, 'aclass': aclass}

        response = self._api.query_private('private/DepositAddress', params=q)
        return response

    def deposit_status(self, asset, method, aclass='currency'):
        """
        Query a deposit's status, by passed asset and method.
        :param asset:
        :param method:
        :param aclass:
        :return:
        """
        q = {'asset': asset, 'method': method, 'aclass': aclass}

        response = self._api.query_private('private/DepositStatus', params=q)
        return response

    def withdraw_info(self, asset, key, amount, aclass='currency'):
        """
        Return withdraw information from user account.
        :param asset:
        :param key:
        :param amount:
        :param aclass:
        :return:
        """
        q = {'asset': asset, 'key': key, 'amount': amount, 'aclass': aclass}

        response = self._api.query_private('private/WithdrawInfo', params=q)
        return response

    def withdraw(self, asset, key, amount, aclass='currency'):
        """
        Withdraw funds from user account by passed asset, key and amount.
        :param asset:
        :param key:
        :param amount:
        :param aclass:
        :return:
        """
        q = {'asset': asset, 'key': key, 'amount': amount, 'aclass': aclass}

        response = self._api.query_private('private/Withdraw', params=q)
        return response

    def withdraw_status(self, asset, aclass='currency', method=None):
        """
        Query status of a withdrawal by passed asset.
        :param asset:
        :param aclass:
        :param method:
        :return:
        """
        q = {'asset': asset, 'aclass': aclass}
        if method is not None:
            q['method'] = method

        response = self._api.query_private('private/WithdrawStatus', params=q)
        return response

    def withdrawal_cancel(self, asset, refid, aclass='currency'):
        """
        Cancel a withdrawal by passed asset and refid.
        :param asset:
        :param refid:
        :param aclass:
        :return:
        """
        q = {'asset': asset, 'refid': refid, 'aclass': aclass}

        response = self._api.query_private('private/WithdrawCancel', params=q)
        return response


if __name__ == '__main__':
    test = KrakenHTTP()
    print(test.ticker('BTCEUR').text)
    print(test.ticker('BTCEUR').text)



