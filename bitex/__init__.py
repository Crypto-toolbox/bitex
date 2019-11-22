"""BitEx is a FOSS library for accessing Crypto-exchange APIs in a convenient way.

It extends :mod:`requests` and implements a standardized set of methods to interact
with exchanges, covering the most commonly used functionality:

    * Acquiring the order book.
    * Acquiring the latest ticker.
    * Acquiring trades.
    * Placing new orders.
    * Cancelling orders.
    * Acquiring an order's status.
    * Fetching a wallet's value.
    * Fetching a wallet's deposit address.
    * Withdrawing coins from the wallet.

Additionally, it provides the option to request endpoints which are not one of the
above using a shorthand.


.. Note::

    The implementation of additional methods and their naming is dependent on
    the plugin and its author for the exchange you're accessing.

Diving right in
---------------

A minimal, working example::

    >>>from bitex import BitexSession, BitexAuth
    >>>auth_obj = BitexAuth(key, secret)
    >>>session = BitexSession(auth=auth_obj)
    >>>session.ticker("exchange_name", "BTCUSD")
    <BitexResponse [200 OK]>

If you'd like to access a private endpoint of an API, you'll likely need
a custom :class:`.BitexAuth` class, extending its :meth:`.BitexAuth.__call__` method::


    class BitexAuthSubClass(BitexAuth):
        def __init__(key, secret):
            super(BitexSessionSubclass, self).__init__(auth)

        def __call__(request):
            request.headers = {'SUPER-SECRET': (self.secret_as_bytes + self.key_as_bytes).encode()}
            return request

    >>>auth_obj = BitexAuthSubClass(key, secret)
    >>>session = BitexSession(auth=auth_obj)
    >>>order_options={'price': 100000, 'size': 10, 'type': 'market'}
    >>>session.new_order('exchange_name', "BTCUSD", params=order_options)
    <BitexResponse [200 OK]>

In the example above, we used bitex's set of standardized methods for accessing
the change. However, you may also request data using the bitex short-hand notation.

Making your life easier: the BitEx URL Short-Hand Notation
----------------------------------------------------------

The short-hand notation unifies urls and aims to make using and writing plugins
easier.

The short-hand looks like this::

    <exchange>:<instrument>/<endpoint>[/<action>]

`exchange` refers to the exchange you want to request data from.
`instrument` is either a single `currency` or a currency `pair`.
`endpoint` describes the kind of endpoint you'd like to use:

    * `trades`
    * `book`
    * `ticker`
    * `wallet`
    * `order`

The latter two endpoint types support `actions`, which are listed below:

    * `wallet` actions :

        * `deposit`
        * `withdraw`

      Additionally, a `amount` parameter is always present on the `withdraw` action.

    * `order` actions:

        * `new`
        * `status`
        * `cancel`

The previous examples would look as follows, if they used the shorthand instead::

    >>>auth_obj = BitexAuthSubClass(key, secret)
    >>>session = BitexSession(auth=auth_obj)
    >>>session.get("SomeExchange:ticker/BTCUSD")
    <BitexResponse [200 OK]>
    >>>order_options={'price': 100000, 'size': 10, 'type': 'market'}
    >>>session.post("SomeExchange:BTCUSD/order/new", params=order_options)
    <BitexResponse [200 OK]>

As long as a plugin for `SomeExchange` is installed, :mod:`bitex` will convert the
short-hand to a fully-qualified URL under the hood.
"""
# Home-brew
from bitex.adapter import BitexHTTPAdapter
from bitex.auth import BitexAuth
from bitex.request import BitexPreparedRequest, BitexRequest
from bitex.response import BitexResponse

__version__ = "3.0.0"
