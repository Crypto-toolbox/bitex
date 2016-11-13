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
    try:
        return data['order_id']
    except KeyError:
        return False


def cancel(data, *args, **kwargs):
    return True if 'message' not in data else False


def order_status(data, *args, **kwargs):
    return data['is_live']
