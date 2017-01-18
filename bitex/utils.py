"""
Provides utility functions, used across more than one module or sub module.

"""

# Import Built-Ins
import logging
import json
from functools import wraps

# Import Third-Party
import requests

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


def return_json(formatter=None):
    """
    Decorator, which Applies the referenced formatter to the function output
    (expects requests.response object). If `formatter` is `None`, returns the
    json of the response.
    :param formatter: bitex.formatters.Formatter() obj
    :return: json_data, raw if formatter is None, else formatted_json, raw
    :return type: requests.response.json(), requests.response() obj ||
                  formatted_json, requests.response() obj
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                r = func(*args, **kwargs)
            except Exception:
                log.exception("return_json(): Error during call to %s(%s, %s)",
                              func.__name__, args, kwargs)
                raise

            try:
                r.raise_for_status()
            except requests.HTTPError:
                log.exception("return_json: HTTPError for url %s",
                              r.request.url)
                return None, r

            try:
                data = r.json()
            except json.JSONDecodeError:
                log.exception('return_json: Error while parsing json. '
                              'Request url was: %s, result is: '
                              '%s', r.request.url, r.text)
                return None, r
            except Exception:
                log.exception("return_json(): Unexpected error while parsing "
                              "json from %s", r.request.url)
                raise

            # Apply formatter and return
            if formatter is not None:
                return formatter(data, *args, **kwargs), r
            else:
                return data, r
        return wrapper
    return decorator

