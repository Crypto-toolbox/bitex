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

    def ticker(self, pair):
        pass

    def order_book(self, pair):
        pass

    def trades(self, pair):
        pass

    def balance(self, currency=None):
        pass

    def orders(self):
        pass

    def ledger(self):
        pass

    def add_order(self, prive, vol, pair, ask_or_bid, order_type='limit'):
        pass

    def cancel_order(self, uuid):
        pass

    def deposit_address(self):
        pass

    def withdraw(self, currency, vol, to_address):
        pass

    def fees(self):
        pass