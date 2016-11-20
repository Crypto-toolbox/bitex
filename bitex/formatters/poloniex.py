"""
Task:
Do fancy shit.
"""

# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew

log = logging.getLogger(__name__)


def order_book(data, *args, **kwargs):
    return data


def trade(data, *args, **kwargs):
    try:
        return data['orderNumber']
    except KeyError:
        return False


def cancel(data, *args, **kwargs):
    return True if data['success'] else False
