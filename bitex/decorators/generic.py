"""
Task:
Provides class-independent decorators
"""

# Import Built-Ins
import logging
import time
import json

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


def logging(func):
    def wrapper(self, *args, **kwargs):
        log.debug("%s: Args %s, Kwargs: %s", (func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return wrapper


def validate_response(func):
    def wrapper(self, *args, **kwargs):
        resp = func(*args, **kwargs)

        if resp.status_code != 200:
            raise ConnectionError("Response Code was %s" % resp.status_code)

        try:
            resp.json()
        except json.JSONDecodeError as e:
            log.error("Returned data wasn't json-seriazable - possibly invalid api endpoint? Error: %s", e)
            raise

        return resp
    return wrapper