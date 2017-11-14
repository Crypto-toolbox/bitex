# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.gemini import GeminiREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class Gemini(RESTInterface):
    def __init__(self, **api_kwargs):
        super(Gemini, self).__init__('Gemini', GeminiREST(**api_kwargs))
        raise NotImplementedError
