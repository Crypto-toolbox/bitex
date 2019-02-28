from typing import Union

from urllib3.exceptions import LocationParseError

from requests import Request, PreparedRequest
from requests.packages.urllib3.util import parse_url

from bitex.plugins import PLUGINS
from bitex.constants import BITEX_SHORTHAND_NO_ACTION_REGEX, BITEX_SHORTHAND_WITH_ACTION_REGEX


class BitexPreparedRequest(PreparedRequest):
    def __init__(self, exchange):
        self.exchange = exchange
        super(BitexPreparedRequest, self).__init__()

    @staticmethod
    def check_url_for_shorthand(url):
        """Check if the given URL is a bitex short-hand.

        If it is, we return the value of :meth:`re.Match.groupdict`; otherwise
        we return None instead.
        """
        con_action = BITEX_SHORTHAND_WITH_ACTION_REGEX.match(url)
        sans_action = BITEX_SHORTHAND_NO_ACTION_REGEX.match(url)
        match = con_action or sans_action
        try:
            return match.groupdict()
        except AttributeError:
            # Not a valid shorthand url, return None
            return None


class BitexRequest(Request):

    def __init__(self, private=False, **kwargs):
        super(BitexRequest, self).__init__(**kwargs)
        self.exchange = self.parse_target_exchange()
        self.private = private

    def __repr__(self):
        return f'<BitexRequest [{self.method}]>'

    def parse_target_exchange(self)-> Union[str, None]:
        """Check the URL for its scheme and extract an exchange name, if any.

        If the url starts with http/https we set :attr:`BitexRequest.exchange`
        to `None`. Otherwise we store the `exchange` in said attribute.

        ..Note::

            We do not check whether or not this is an actual exchange name.
            Schemes such as `mailto:` are not checked for and may cause errors.
            Hence, only HTTP urls or :mod:`bitex` short-hand urls are supported
            by :mod:`bitex`!
        """
        try:
            parse_url(self.url).scheme
        except LocationParseError:
            # This string isn't parsable by urllib - it may be a shorthand.
            try:
                scheme, _ = self.url.split(":", maxsplit=1)
                if scheme:
                    return scheme
            except ValueError:
                # Nope, that didn't work. This isn't a known format, return None.
                return None
        else:
            return None

    def prepare(self) -> BitexPreparedRequest:
        """Constructs a :class:`BitexPreparedRequest` for transmission and returns it.

        .. Note::

            Unlike :meth:BitexSession.prepare_request, this method does *not*
            apply a custom auth class automatically, if no auth object was given.
        """
        custom_classes = PLUGINS.get(self.exchange)
        if custom_classes:
            p = custom_classes['PreparedRequest'](self.exchange)
        else:
            p = BitexPreparedRequest(self.exchange)
        p.prepare(
            method=self.method,
            url=self.url,
            headers=self.headers,
            files=self.files,
            data=self.data,
            json=self.json,
            params=self.params,
            auth=self.auth,
            cookies=self.cookies,
            hooks=self.hooks,
        )
        return p
