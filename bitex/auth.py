# Import Built-Ins
import json
import logging
import time

from typing import Tuple, Any, Union, Dict, List
from urllib.parse import parse_qs

# Import Third-party
import requests

from bitex.request import BitexPreparedRequest

# Init Logging Facilities
log = logging.getLogger(__name__)


class BitexAuth(requests.auth.AuthBase):
    """Authentication Meta Class for API authentication.

    Takes care of generating a signature and preparing data sent, headers and
    URLs as required by the exchange this class is subclassed for.

    :param str key: API Key.
    :param str secret: API Secret.
    """

    def __init__(self, key: str, secret: str) -> None:
        self.key = key
        self.secret = secret

    @property
    def key_as_bytes(self) -> bytes:
        """Return the key encoded as bytes.

        :rtype: bytes
        """
        return self.key.encode('utf-8')

    @property
    def secret_as_bytes(self) -> bytes:
        """Return the secret encoded as bytes.

        :rtype: bytes
        """
        return self.secret.encode('utf-8')

    def __call__(self, request: BitexPreparedRequest) -> BitexPreparedRequest:
        """Sign the given request.

        This must be extended in subclasses as it merely returns the request and
        does not do any signing / authentication.

        :param requests.PreparedRequest request: The prepared request to sign.
        :rtype: requests.PreparedRequest
        """
        return request

    @staticmethod
    def decode_body(request: BitexPreparedRequest) -> Union[Dict, Tuple[Tuple[str, List[Any]], ...]]:
        """Decode the urlencoded body of the given request and return it.

        Some signature algorithms require us to use the body. Since the body is
        already urlencoded by requests.PreparedRequest.prepare(), we need to undo
        its work before returning the request body's contents.

        We must accomodate for the case that in some cases the body may be a
        JSON encoded string. We expect the parsed JSON to be a dictionary of
        objects. Should the body be an encoded list, this method will raise
        an :exc:`AttributeError`.

        :param BitexPreparedRequest request:
            The request whose body we should decode.
        :rtype: Tuple[Tuple[str, str], ...]
        """
        if request.headers["Content-Type"] == 'application/json':
            # The body is required to be bytes, so we decode to string first
            body = request.body.decode("UTF-8")
            body_as_dict = json.loads(body, parse_int=str, parse_float=str)
            body_as_dict = {k: [v] for k,v in body_as_dict.items()}
        else:
            body_as_dict = parse_qs(request.body)
        print(body_as_dict)
        items = body_as_dict.items()
        return tuple(
            (key, value)
            for key, value in sorted(items, key=lambda x: x[0])
        )

    @staticmethod
    def nonce() -> str:
        """Create a Nonce value for signature generation.

        By default, this is a unix timestamp with millisecond resolution.

        converted to a str.
        :return: Nonce
        :rtype: str
        """
        return str(int(round(1000 * time.time())))
