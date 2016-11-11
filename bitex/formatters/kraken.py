"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew

log = logging.getLogger(__name__)


def trade(data):
    return data['result']['txid']


def order_book(data):
    return data['result']


def cancel(data):
    if int(data['result']['count']) == 1:
        return True
    else:
        return False
