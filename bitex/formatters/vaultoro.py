# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class VaultoroFormatter(Formatter):

    def format_pair(self, input_pair):
        base, quote = super(VaultoroFormatter, self).format_pair(input_pair)
        return base.lower() + quote.lower()
