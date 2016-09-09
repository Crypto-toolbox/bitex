# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

It provides primarily REST-based clients for a variety of Crypto exchanges. It handles authentication and requests to common endpoints via convenience methods, 
as well as granting access to all other endpoint via the low level api interface.

# State
--------------------------------

**API** : **Completed**

**Clients** : **WIP**

--------------------------------
As of now, only REST APIs are supported, implementations of websockets and FIX connections are being considered.

The following exchanges are supported

REST-based APIs:
- GDAX (implemented)
- Bitfinex (implemented)
- Bitstamp (implemented)
- Kraken (implemented)
- Coincheck (public endpoint communication done)
- OKCoin (public endpoint communication done)
- BTC-E (public endpoint communication done) [DEPRECATED] - Too shitty support, pardon my french.
- Bittrex (public endpoint communication done)
- C-CEX (public endpoint communication done)
- Cryptoptia (public endpoint communication done)
- Yunbi (public endpoint communication done)
- Gemini (public endpoint communication done)
- TheRockTradingLTD (public endpoint communication done)


-`planned`: I'm currently designing base code for this exchange

-`public endpoint communication done`: You're able to communicate with the API using its respective API class with `public` endpoints only.

-`implemented`: Authentication protocols have been implemented and the class' `query()` method supports the `authenticate=True` flag



Additional clients will be added to (or removed from) this list, according to their liquidity and market volume.

In their basic form, clients provide a simple connection to APIs - that is, they handle authentication and request construction for you. As soon the above list is completed to a point where most of the exchanges are implemented (or whenever I feel like it), I will add convenience layers to the clients; this layer will aim to make calling the api feel more like a function, instead of string construction (i.e. `kraken.ticker('XBTEUR')`, instead of typing `kraken.public_query({'pair': 'XBTEUR'})`). 

# REST APIs

The above listed exchanges all have an implemented API class in `bitex.api`. These provide low-level access to the
respective exchange's REST API, including handling of authentication. They do not feature convenience methods, so you will
have to write some things yourself. 

At their core, they can be thought of as simple overlay methods for `requests.request()` methods, as all
kwargs passed to query, are also passed to these methods as well. They simply handle the exchange's authentication protocols as well.

An example:
```
from bitex.api.rest import KrakenREST

k = KrakenREST()
k.load_key('kraken.key')

k.query('GET','public/Depth', params={'pair': 'XXBTZUSD'})
k.query('POST','private/AddOrder', authenticate=True,
        params={'pair': 'XXBTZUSD', 'type': 'sell', 'ordertype': 'limit',
                'price': 1000.0, 'volume': 0.01, 'validate': True})
```

# Installation
`python3 setup.py install`


# Usage
Import any client from the `http` submodule.
```
from bitex.http import KrakenHTTP
uix = KrakenREST()
uix.order_book('XBTEUR')
```

If you'd like to query a private endpoint, you'll have to either supply your secret & api keys like this:
```
uix = KrakenREST(key='your-api-key-here', secret='your-api-secret-here')
```

Or, which I'd recommend for safety and convenience reasons, pass a keyfile containing your api and secret on a seperate line each (Note: some clients require additional args to authenticate! These should come before the api and secret in the file!):
```
>my_api.key
513423534dljr1234  # Api key
knjer23053n90d02d3nd90d23d23d==  # Api Secret

>main.py
from bitex.http import KrakenREST
uix = KrakenHTTP(key_file='./my_api.key')
```






