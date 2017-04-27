# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class BtstFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(BtstFormatter, self).format_pair(input_pair)
        return base.lower() + quote.lower()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'], data['open'],
                None, data['last'], data['volume'], data['timestamp'])


