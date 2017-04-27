# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class CcexFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(CcexFormatter, self).format_pair(input_pair)
        return base.lower() + '-' + quote.lower()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['buy'], data['sell'], data['high'], data['low'], None,
                None, data['lastprice'], None, data['updated'])