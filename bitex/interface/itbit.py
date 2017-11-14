# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.itbit import ITbitREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class ItBit(RESTInterface):
    def __init__(self, **api_kwargs):
        super(ItBit, self).__init__('itBit', ITbitREST(**api_kwargs))
        raise NotImplementedError
