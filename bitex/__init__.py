"""Bitex Core Module.

Provides abstract base classes for accessing crypto-exchange REST APIs.

Each class is required to access an exchange's API, and must be subclassed before usage.

A minimal, working example::

    from bitex import BitexSession, BitexAuth

    class BitexAuthSubClass(BitexAuth):
        def __init__(key, secret):
            super(BitexSessionSubclass, self).__init__(auth)

        def __call__(request):
            request.headers = {'SUPER-SECRET': (self.secret_as_bytes + self.key_as_bytes).encode()}

    class BitexSessionSubclass(BitexSession):
        pass

In action::

    >>>auth_obj = BitexAuthSubclass(key, secret)
    >>>session = BitexSessionSubclass(auth=auth_obj)
    >>>session.ticker("exchange_name", "BTCUSD")
    <requests.BitexResponse [200]>

"""
from bitex.request import BitexRequest, BitexPreparedRequest
from bitex.response import BitexResponse
from bitex.auth import BitexAuth
from bitex.adapter import BitexHTTPAdapter


__version__ = "3.0.0"
