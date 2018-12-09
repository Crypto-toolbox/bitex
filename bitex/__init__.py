"""API Meta Classes for bitex_rest_api.

Each class is required to access an exchange's API, and must be subclassed before usage.

A minimal, working example::

    from bitex_rest_api.base import BitexAPIABC, BitexSessionABC, BitexAuthABC

    class BitexAuthSubClass(BitexAuthABC):
        def __init__(key, secret):
            super(BitexSessionSubclass, self).__init__(auth)

        def __call__(request):
            request.headers = {'SUPER-SECRET': (self.secret_as_bytes + self.key_as_bytes).encode()}


    class BitexSessionSubclass(BitexSessionABC):
        def __init__(key, secret):
            auth = BitexAuthSubclass(key, secret)
            super(BitexSessionSubclass, self).__init__(auth)


    class BitexAPISubclass(BitexAPIABC):
        def __init__(key, secret):
            private_session = BitexSessionSubclass(key, secret)
            addr = 'https://myexchange.io/api'
            version = 'v1'
            timeout = 12
            super(BitexSessionSubclass, self).__init__(addr, version, timeout, auth)

We subclass the ABC classes defined in this file, and add a custom header to the request in
BitexAusSubclass's __call__() method. This is added to all requests made to private endpoints
(triggered by passing the 'private=True' kwarg to  BitexAPISubclass's get(), put(), post(), etc.
methods).

"""
from bitex_rest_api.base.auth import BitexAuthABC
from bitex_rest_api.base.session import BitexSessionABC
from bitex_rest_api.base.adapter import BitexAdapter
from bitex_rest_api.base.response import BitexResponseABC
from bitex_rest_api.base.api import BitexAPIABC
