"""Hook Implementation for :mod:`bitex`'s plugin system.

This serves both as the fall-back default, as well as a reference implementation
of the hook specs.
"""
# Built-in
from typing import Mapping, Tuple, Type, Union

# Third-party
import pluggy
from requests import PreparedRequest, Response
from requests.auth import HTTPBasicAuth

hookimpl = pluggy.HookimplMarker("bitex-core")


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
    """Since bitex is exchange-agnostic at its core, we return `None`.

    Returning `None` causes :mod:`bitex` to leave the given url untouched and
    pass it on to the :mod:`requests` components as is.
    """
    return None
