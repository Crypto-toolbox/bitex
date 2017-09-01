"""
Contains all custom Warnings and Exceptions used in BitEx
"""
# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


class IncompleteCredentialsWarning(UserWarning):
    """Raised when a required parameter for authentication (for example key or
    secret) is not given upon initialization of an API object."""
    pass


class IncompleteCredentialConfigurationWarning(UserWarning):
    """Raised when a required parameter for authentication (for example key or
    secret) is not found in a given config file upon calling load_config()."""
    pass


class IncompleteCredentialsError(Exception):
    """Raised when attempting to call private_query() of an API, but we're
    still missing essential values to create a message signature (key, secret
    or additional other values, dependent on the exchange)."""
    pass


class IncompleteAPIConfigurationWarning(UserWarning):
    """Raised if either the version or address key word is not found in a
    given config file when load_config() is called."""
    pass


class EmptySupportedPairListWarning(UserWarning):
    """Raised when _supported_pairs is Empty or None while querying an API"""
    pass


class UnsupportedPairError(ValueError):
    """Raised if a given pair isn't supported by an Interface / API."""


class UnsupportedEndpointError(AttributeError):
    """Raised if a call to an API method, which is not supported by the currently
    configured API Version, is made"""
