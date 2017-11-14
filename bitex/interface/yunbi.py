"""Yunbi Interface class."""
# pylint: disable=abstract-method
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.yunbi import YunbiREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class Yunbi(RESTInterface):
    """Yunbi Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(Yunbi, self).__init__('Yunbi', YunbiREST(**api_kwargs))
        raise NotImplementedError
