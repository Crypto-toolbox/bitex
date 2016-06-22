"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import time
# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)



def time_resp(func):
    def wrapper(self, *args, **kwargs):
        sent = time.time()
        try:
            resp, pair = func(self, *args, **kwargs)
            received = time.time()
            return sent, received, resp, pair
        except ValueError:
            resp = func(self, *args, **kwargs)
            received = time.time()
            return sent, received, resp
    return wrapper
