# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class PlnxFormatter(Formatter):

    @staticmethod
    def order(data, *args, **kwargs):
        try:
            return data['orderNumber']
        except KeyError:
            return False

    @staticmethod
    def cancel(data, *args, **kwargs):
        return True if data['success'] else False
