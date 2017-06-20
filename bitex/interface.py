# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from .pairs import PairFormatter
from .exceptions import UnsupportedPairError
# Init Logging Facilities
log = logging.getLogger(__name__)


class Interface:
    def __init__(self, name, rest_api):
        self.REST = rest_api
        self.name = name
        self._supported_pairs = self._get_supported_pairs()

    @property
    def supported_pairs(self):
        return self._supported_pairs

    def _get_supported_pairs(self):
        """Generate a list of supported pairs.

        Queries the API for a list of supported pairs and returns this as a
        list.

        Raises a NotImplementedError by default and needs to be overridden in
        child classes.

        :raises: NotImplementedError
        """
        raise NotImplementedError

    def is_supported(self, pair):
        """Checks if the given pair is present in self._supported_pairs.

        Input can either be a string or a PairFormatter Obj (or child thereof).
        If the latter two, we'll call the format() method with the Interface's
        name attribute to acquire proper formatting.
        If it's not a pair, we'll raise an UnsupportedPairError.

        :param pair: Str, or PairFormatter Object
        :return: Bool
        :raise: UnsupportedPairError
        """
        if isinstance(pair, PairFormatter):
            return True if pair.format(self.name) in self._supported_pairs else False
        else:
            return True if pair in self._supported_pairs else False

    def _request(self, pair, endpoint, **req_kwargs):
        self.is_supported(pair)
        return self.REST._query(endpoint, **req_kwargs)


