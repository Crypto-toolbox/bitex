# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class YnbiFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(YnbiFormatter, self).format_pair(input_pair)
        return base.lower() + '_' + quote.lower()

    @staticmethod
    def ticker(data, *args, **kwargs):
        date = data['at']
        data = data['ticker']
        return (data['buy'], data['sell'], data['high'], data['low'],
                None, None, data['last'], data['vol'], date)