"""Gemini Interface class."""
# pylint: disable=abstract-method
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.gemini import GeminiREST
from bitex.interface.rest import RESTInterface


# Init Logging Facilities
log = logging.getLogger(__name__)


class Gemini(RESTInterface):
    """Gemini Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(Gemini, self).__init__('Gemini', GeminiREST(**api_kwargs))
        raise NotImplementedError
