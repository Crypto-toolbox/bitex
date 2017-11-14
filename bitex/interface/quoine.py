# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.quoine import QuoineREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class Quoine(RESTInterface):
    def __init__(self, **APIKwargs):
        super(Quoine, self).__init__('Quoine', QuoineREST(**APIKwargs))
        raise NotImplementedError
