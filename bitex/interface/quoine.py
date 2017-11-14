"""Quoine Interface class."""
# pylint: disable=abstract-method
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.quoine import QuoineREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class Quoine(RESTInterface):
    """Quoine Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(Quoine, self).__init__('Quoine', QuoineREST(**api_kwargs))
        raise NotImplementedError
