""":mod:``bitex`` extension for :cls:``requests.Request`` &  :cls:``requests.PreparedRequest`` classes."""
# Built-in
from typing import Union

# Third-party
from requests import PreparedRequest, Request
from requests.packages.urllib3.util import parse_url

# Home-brew
from bitex.constants import BITEX_SHORTHAND_NO_ACTION_REGEX, BITEX_SHORTHAND_WITH_ACTION_REGEX
from bitex.plugins import PLUGINS
from bitex.types import RegexMatchDict


class BitexPreparedRequest(PreparedRequest):
    """Bitex extension of :cls"``requests.PreparedRequest``.

    Implements a checker function for short-hand urls.
    """

    def __init__(self, exchange):
        self.exchange = exchange
        super(BitexPreparedRequest, self).__init__()

    @staticmethod
    def check_url_for_shorthand(url) -> Union[RegexMatchDict, None]:
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
    """Bitex extension of :cls"``requests.Request``.

    Implements a parser function for exchange names from a given URL.

    Additionally re-implements :meth:``requests.Request.prepare``, replacing
    the instantiation of the ``requests.PreparedRequest`` class with an
    instance of :cls:``.BitexPreparedRequest``.
    """

    def __init__(self, private: bool = False, **kwargs) -> None:
        super(BitexRequest, self).__init__(**kwargs)
        self.exchange = self.parse_target_exchange()
        self.private = private

    def __repr__(self) -> str:
        """Extend original class's __repr__."""
        return f"<BitexRequest [{self.method}]>"

    def parse_target_exchange(self) -> Union[str, None]:
        """Check the URL for its scheme and extract an exchange name, if any.

        If the url starts with http/https we set :attr:`BitexRequest.exchange`
        to `None`. Otherwise we store the `exchange` in said attribute.
        """
        scheme = parse_url(self.url).scheme
        if scheme and not scheme.startswith("http"):
            return scheme
        return None

    def prepare(self) -> BitexPreparedRequest:
        """Construct a :class:`BitexPreparedRequest` for transmission and return it.

        .. Note::

            Unlike :meth:BitexSession.prepare_request, this method does *not*
            apply a custom auth class automatically, if no auth object was given.
        """
        custom_classes = PLUGINS.get(self.exchange)
        if custom_classes:
            p = custom_classes["PreparedRequest"](self.exchange)
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
