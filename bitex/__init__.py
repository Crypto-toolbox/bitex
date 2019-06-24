"""Bitex-Core Module.

Provides base classes for accessing crypto-exchange REST APIs in a convenient way.

A minimal, working example::

    >>>from bitex import BitexSession, BitexAuth
    >>>auth_obj = BitexAuth(key, secret)
    >>>session = BitexSession(auth=auth_obj)
    >>>session.ticker("exchange_name", "BTCUSD")
    <requests.BitexResponse [200]>

If you'd like to access private endpoint of an API, you'll likely need
a custom :cls:`.BitexAuth` class, extending its :meth:`.BitexAuth.__call__` method::


    class BitexAuthSubClass(BitexAuth):
        def __init__(key, secret):
            super(BitexSessionSubclass, self).__init__(auth)

        def __call__(request):
            request.headers = {'SUPER-SECRET': (self.secret_as_bytes + self.key_as_bytes).encode()}

    >>>auth_obj = BitexAuthSubClass(key, secret)
    >>>session = BitexSession(auth=auth_obj)
    >>>order_options={'price': 100000, 'size': 10, 'type': 'market'}
    >>>session.new_order('exchange_name', "BTCUSD", params=order_options)

"""
# Home-brew
from bitex.adapter import BitexHTTPAdapter
from bitex.auth import BitexAuth
from bitex.request import BitexPreparedRequest, BitexRequest
from bitex.response import BitexResponse

__version__ = "3.0.0-dev"
