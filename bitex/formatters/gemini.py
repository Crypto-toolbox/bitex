# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class GmniFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(GmniFormatter, self).format_pair(input_pair)
        return base.lower() + quote.lower()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], None, None, None, None, data['last'],
                data['volume'][args[0][:3].upper()], data['volume']['time'])