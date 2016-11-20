"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew

log = logging.getLogger(__name__)


def trade(data, *args, **kwargs):
    if data['success']:
        return data['result']['uuid']
    else:
        return False


def order_book(data, *args, **kwargs):
    if data['success']:
        return data['result']
    else:
        return None


def cancel(data, *args, **kwargs):
    return True if data['success'] else False
