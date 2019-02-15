"""API Abstract Base Classes for bitex.

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

    >>>auth_obj = BitexAuthSubclass(key, secret)
    >>>session = BitexSessionSubclass(auth=auth_obj)
    >>>session.ticker("exchange_name", "BTCUSD")
    <requests.BitexResponse [200]>



We subclass the ABC classes defined in this file, and add a custom header to the request in
BitexAuthSubclass's __call__() method. This is added to all requests made to private endpoints.

"""
from bitex.request import BitexRequest, BitexPreparedRequest
from bitex.response import BitexResponse
from bitex.auth import BitexAuth
from bitex.adapter import BitexHTTPAdapter





