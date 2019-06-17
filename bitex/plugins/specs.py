"""Hook Specifications for :mod:`bitex`'s plugin system."""
# Built-in
from typing import Mapping, Tuple, Type, Union

# Third-party
import pluggy
from requests import PreparedRequest, Response
from requests.auth import AuthBase

hookspec = pluggy.HookspecMarker("bitex")


@hookspec
def announce_plugin() -> Union[
    Tuple[str, Type[AuthBase], Type[PreparedRequest], Type[Response]], None
]:
    """Announce plugin classes to :mod:`bitex`.

    The function should return a Tuple[str, Type[AuthBase], Type[PreparedRequest].
    Where str is the exchange this plugin belongs to, followed by the auth and
    prepared requests class to use when requesting stated exchange.
    """
