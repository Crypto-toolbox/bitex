from requests.models import Response


class BitexResponse(Response):
    """Custom Response class."""

    def __repr__(self):
        return '<BitexResponse [%s]>' % (self.status_code)

    def triples(self):
        """Return the data of the response in three-column layout.

        Data is returned as a list of 3-item tuples::

            [
                (<timestamp>, <label>, <value>),
                (<timestamp>, <label>, <value>),
                ...
            ]
        """
        raise NotImplementedError

    def key_value_dict(self):
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
