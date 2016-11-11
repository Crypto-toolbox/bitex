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
    return data['orderNumber']

def cancel(data):
    return True if data['success'] else False
