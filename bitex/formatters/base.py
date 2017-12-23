"""Base class for formatters."""

import requests
from collections import namedtuple

"""The base class that each formatter has to implement.

It adds a `formatted` property, which returns a namedtuple with data
converted from the json response.
"""


class AbstractFormattedResponse(requests.Response):

    def __init__(self, response_obj):
        self.response = response_obj

    @property
    def formatted(self):
        raise NotImplementedError

    def __getattr__(self, attr):
        """Use methods of the encapsulated object, when not available in the wrapper."""
        return getattr(self.response, attr)


# Every formatter should return a tuple with the same structure, so that data can be managed in
# the same "standard" way for every exchange.
FormattedResponseTuple = namedtuple("FormattedResponse", ("bid",
                                                          "ask",
                                                          "high",
                                                          "low",
                                                          "last",
                                                          "volume",
                                                          "timestamp"))
