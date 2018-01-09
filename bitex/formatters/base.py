"""Base class for formatters."""

import requests
from collections import namedtuple

"""The base class that each formatter has to implement.

It adds a `formatted` property, which returns a namedtuple with data
converted from the json response.
"""


class AbstractFormattedResponse(requests.Response):

    def __init__(self, method, response_obj, *args, **kwargs):
        self.response = response_obj
        self.method = method
        self.method_args = args
        self.method_kwargs = kwargs

    def __getattr__(self, attr):
        """Use methods of the encapsulated object, otherwise use what available in the wrapper."""
        try:
            return getattr(self.response, attr)
        except AttributeError:
            return getattr(self, attr)

    @property
    def formatted(self):
        """Return the formatted data, extracted from the json response."""
        return getattr(self, self.method)

    def ticker(*args, **kwargs):
        raise NotImplementedError

    def order_book(*args, **kwargs):
        raise NotImplementedError

    def trades(*args, **kwargs):
        raise NotImplementedError

    def bid(*args, **kwargs):
        raise NotImplementedError

    def ask(*args, **kwargs):
        raise NotImplementedError


# Every method should return a tuple with the same structure, so that data can be managed in the
# same "standard" way for every exchange.
TickerFormattedResponseTuple = namedtuple("TickerResponse", ("bid",
                                                             "ask",
                                                             "high",
                                                             "low",
                                                             "last",
                                                             "volume",
                                                             "timestamp"))
