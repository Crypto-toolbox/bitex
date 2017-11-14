# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.yunbi import YunbiREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class Yunbi(RESTInterface):
    def __init__(self, **api_kwargs):
        super(Yunbi, self).__init__('Yunbi', YunbiREST(**api_kwargs))
        raise NotImplementedError
