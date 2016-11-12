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
    try:
        return data['orderNumber']
    except KeyError:
        return False


def cancel(data):
    return True if data['success'] else False
