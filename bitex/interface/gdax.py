"""GDAX Interface class."""
# pylint: disable=abstract-method
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.gdax import GDAXREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class GDAX(RESTInterface):
    """GDAX Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(GDAX, self).__init__('GDAX', GDAXREST(**api_kwargs))
        raise NotImplementedError
