"""Hook Implementation for :mod:`bitex`'s plugin system."""
import pluggy

from typing import Union, Tuple, Type, Mapping
from requests.auth import HTTPBasicAuth
from requests import PreparedRequest, Response

hookimpl = pluggy.HookimplMarker("bitex")


@hookimpl
def announce_plugin() -> Union[
    Tuple[str, Type[HTTPBasicAuth], Type[PreparedRequest], Type[Response]], None
]:
    """By default we return an AuthBase and PreparedRequest class.

    These classes will never be actually used, since the exchange "base" does not
    exist and is never contacted. However, it serves as a simple example on what
    this hook function is supposed to return.
    """
    return "base", HTTPBasicAuth, PreparedRequest, Response


@hookimpl
def construct_url_from_shorthand(match_dict: Mapping[str, str]) -> Union[str, None]:
    return None
