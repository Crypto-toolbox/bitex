# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

It provides API classes for various REST-based APIs for a variety of 
crypto exchanges. It handles authentication as well as granting access to 
all endpoints via the low level api interface.


# State
--------------------------------

**API** : **Completed**

**Clients** : **WIP**

--------------------------------
As of now, only REST APIs are supported, implementations of websockets 
and FIX connections are being considered.

The following exchanges are supported

REST-based APIs:
- GDAX (implemented)
- Bitfinex (implemented)
- Bitstamp (implemented)
- Kraken (implemented)
- itBit (public endpoint communication done)
- Coincheck (public endpoint communication done)
- OKCoin (public endpoint communication done)
- BTC-E (public endpoint communication done) [DEPRECATED]
- Bittrex (public endpoint communication done)
- C-CEX (public endpoint communication done)
- Cryptoptia (public endpoint communication done)
- Yunbi (public endpoint communication done)
- Gemini (public endpoint communication done)
- TheRockTradingLTD (public endpoint communication done)
- Poloniex (public endpoint communication done)


-`planned`: I'm currently designing base code for this exchange

-`public endpoint communication done`: You're able to communicate with 
the API using its respective API class with `public` endpoints only.

-`implemented`: Authentication protocols have been implemented and the 
class' `query()` method supports the `authenticate=True` flag



Additional clients will be added to (or removed from) this list, 
according to their liquidity and market volume.

In their basic form, clients provide a simple connection to APIs - that 
is, they handle authentication and request construction for you. The 
classes in `bitex.interfaces` provide additional convenience methods.
They offer unified methods across all exchanges (i.e. order_book(), 
ticker(), trades(), among others), and parse returned data sensibly.

All methods return a tuple of parsed data and the original 
response object.

For example, the return values for 
`bitex.interfaces.Kraken.ask(*args, **kwargs)` is a tuple of 
`(<transaction_id>, <response object>)`.


# REST APIs

The above listed exchanges all have an implemented API class in 
`bitex.api`. These provide low-level access to the
respective exchange's REST API, including handling of authentication. 
They do not feature convenience methods, so you will
have to write some things yourself. 

At their core, they can be thought of as simple wrapper methods for 
`requests.request()` methods which additionally handle the bits and pieces
of the exchanges authentication protocol as well.

An example:
```
from bitex.api.rest import KrakenREST

k = KrakenREST()
k.load_key('kraken.key')  # loads key and secret from given file;

# Poll order book for XBTUSD
q = {'pair': 'XXBTZUSD'}
k.query('GET','public/Depth', params=q)  # without auth

# Place ask order (requires authentication
q = {'pair': 'XXBTZUSD', 'type': 'sell', 'ordertype': 'limit',
     'price': 1000.0, 'volume': 0.01, 'validate': True}
k.query('POST','private/AddOrder', authenticate=True, params=q) 

```

Example `.key` file:
```
>>>dummy.key
my_api_key
my_fancy_api_secret
```

If the api requires further details, for example a userid or account 
number (for example for bitstamp), this needs to go before the api key 
and secret, on a separate line each.
```
>>>dummy2.key
Userid
accountname
my_api_key
my_fancy_api_secret
```


# Installation
`python3 setup.py install`

or via pip
`pip install BitEx`









