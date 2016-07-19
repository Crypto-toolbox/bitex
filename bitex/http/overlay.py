"""
Task:
This is a Reference for HTTP Clients. It's mostly for developers, to keep
track of what methods should / need to be implemented, and what methods
should be available to make their client work with the package.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self):
        pass

    def ticker(self, pair, **kwargs):
        """
        Returns Ticker of given pair
        :param pair:
        :param kwargs:
        :return:
        """
        pass

    def order_book(self, pair, **kwargs):
        """
        Returns order book for given pair.
        :param pair:
        :param kwargs:
        :return:
        """
        pass

    def trades(self, pair, **kwargs):
        """
        Returns recent trades for given pair.
        :param pair:
        :param kwargs:
        :return:
        """
        pass

    def balance(self, **kwargs):
        """
        Returns the balance of the exchange account's wallets.
        :param kwargs:
        :return:
        """
        pass

    def orders(self, *args, **kwargs):
        """
        Return open orders.
        :param pair:
        :param kwargs:
        :return:
        """
        pass

    def ledger(self):
        """
        Ledger consists of recent trades, deposits, and withdrawals to and
        from user's account.
        :return:
        """
        pass

    def add_order(self, prive, vol, pair, ask_or_bid, order_type='limit',
                  **kwargs):
        """
        Places a bid or ask order of given order type.
        :param prive:
        :param vol:
        :param pair:
        :param ask_or_bid:
        :param order_type:
        :param kwargs:
        :return:
        """
        pass

    def cancel_order(self, uuid):
        """
        cancels an order with the given uuid.
        :param uuid:
        :return:
        """
        pass

    def fees(self):
        """
        Returns fees applicable at exchange.
        :return:
        """
        pass