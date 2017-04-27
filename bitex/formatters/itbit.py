# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class itbtFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(itbtFormatter, self).format_pair(input_pair)
        return base.upper() + quote.upper()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high24h'], data['low24h'],
                data['openToday'], None, data['lastPrice'], data['volume24h'],
                data['serverTimeUTC'])