# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class GdaxFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(GdaxFormatter, self).format_pair(input_pair)
        return base.upper() + '-' + quote.upper()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], None, None, None, None, data['price'],
                data['volume'], data['time'])