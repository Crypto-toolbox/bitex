"""Hook Specifications for :mod:`bitex`'s plugin system."""
import pluggy

from typing import Union, Tuple, Type, Mapping
from requests.auth import AuthBase
from requests import PreparedRequest, Response

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
