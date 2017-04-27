# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class RockFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(RockFormatter, self).format_pair(input_pair)
        return base.upper() + quote.upper()

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'],
                data['open'], data['close'], data['last'],
                data['volume_traded'], data['date'])