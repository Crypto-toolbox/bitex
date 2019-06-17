"""Customized :cls:``requests.Response`` class for the :mod:``bitex`` framework."""
# Built-in
from typing import List

# Third-party
from requests.models import Response

# Home-brew
from bitex.types import KeyValuePairs, Triple


class BitexResponse(Response):
    """Custom :cls:``requests.Response`` class.

    Supplies additional format outputs of the underlying `JSON` data, as returned
    by :meth:``.json``.
    """

    def __repr__(self):
        """Extend original class's __repr__."""
        return f"<{self.__class__.__qualname__} [{self.status_code}]>"

    def triples(self) -> List[Triple]:
        """Return the data of the response in three-column layout.

        Data is returned as a list of 3-item tuples::

            [
                (<timestamp>, <label>, <value>),
                (<timestamp>, <label>, <value>),
                ...
            ]
        """
        raise NotImplementedError

    def key_value_dict(self) -> KeyValuePairs:
        """Return the data of the response in a flattened dict.

        This provides the data as a dict of key-value pairs, which is ready for
        consumption by libraries such as pandas::

            {
                <label>: <value>,
                <label>: <value>,
                ...
            }
        """
        raise NotImplementedError
