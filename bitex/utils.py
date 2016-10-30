# Import Built-Ins
import logging
import json
# Import Third-Party

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


def return_json(func):
    """
    Wrapper to add additional debugging information to response objects.

    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
        except Exception as e:
            log.error("return_json(): Error during call to %s(%s, %s) %s" % (func.__name__, args, kwargs, e))
            raise

        if r.status_code != 200:
            log.error("return_json: Error while querying %s" % r.request.url)
            raise ConnectionError("Returned Status Code was %s" % r.status_code)

        try:
            return r.json()
        except json.JSONDecodeError:
            log.error('return_json: Error while parsing json. '
                      'Request url was: %s, result is: %s' % (r.request.url, r.text))
            return None
        except Exception as e:
            log.error("return_json(): Unexpected error while parsing json from %s: %s" % (r.request.url, e))
    return wrapper
