# Import Built-Ins
import logging
import warnings

# Import Third-Party

# Import Homebrew
from .pairs import PairFormatter
from .exceptions import UnsupportedPairError, EmptySupportedPairListWarning
# Init Logging Facilities
log = logging.getLogger(__name__)


class Interface:
    def __init__(self, *, name, rest_api):
        self.REST = rest_api
        self.name = name
        try:
            self._supported_pairs = self._get_supported_pairs()
        except NotImplementedError:
            self._supported_pairs = None

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
        """
        if pair.format(self.name) in self._supported_pairs:
            return True
        else:
            return False

    def request(self, verb, pair, endpoint, authenticate=False, **req_kwargs):
        """Query the API and return its result.

        :param verb: HTTP verb (GET, PUT, DELETE, etc)
        :param pair: Str or PairFormatter Obj
        :param endpoint: Str
        :param authenticate: Bool, whether to call private_query or public_query
                             method.
        :param req_kwargs: Kwargs to pass to _query / requests.request()
        :raise: UnsupportedPairError
        :return: requests.Response() Obj
        """
        if not self._supported_pairs:
                warnings.warn("No list of valid pairs available! Check that "
                              "_get_supported_pairs() is implemented and "
                              "returns a Non-empty list!",
                              EmptySupportedPairListWarning)
        elif not self.is_supported(pair):
            raise UnsupportedPairError

        if authenticate:
            return self.REST.private_query(verb, endpoint, **req_kwargs)
        else:
            return self.REST.public_query(verb, endpoint, **req_kwargs)



