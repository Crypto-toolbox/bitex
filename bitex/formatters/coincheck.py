# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class CnckFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(CnckFormatter, self).format_pair(input_pair)
        return base.lower() + '_' + quote.lower()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'], None, None,
                data['last'], data['volume'], data['timestamp'])