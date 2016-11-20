# Import Built-Ins
import logging
import json
import requests
# Import Third-Party

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


def return_json(formatter=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                r = func(*args, **kwargs)
            except Exception as e:
                log.error("return_json(): Error during call to "
                          "%s(%s, %s) %s" % (func.__name__, args, kwargs, e))
                raise

            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                log.error("return_json: HTTPError for url %s: "
                          "%s" % (r.request.url, e))
                return None, r

            try:
                data = r.json()
            except json.JSONDecodeError:
                log.error('return_json: Error while parsing json. '
                          'Request url was: %s, result is: '
                          '%s' % (r.request.url, r.text))
                return None, r
            except Exception as e:
                log.error("return_json(): Unexpected error while parsing json "
                          "from %s: %s" % (r.request.url, e))
                raise

            # Apply formatter and return
            if formatter is not None:
                return formatter(data, *args, **kwargs), r
            else:
                return data, r
        return wrapper
    return decorator

