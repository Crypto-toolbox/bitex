# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

This project evolved out of the pure pleasure of writing clients for REST APIs, and a want and need for a single data stream to read from for my bitcoin bots. 

# What is BitEx

Bitex provides primarily REST-based clients for a variety of Crypto exchanges. It comes packaged with a publish-subscribe module, which allows easy polling and distribution of exchange data to, for example, an automated trading strategy.

# State

As of now, only REST APIs are supported, implementations of websockets and FIX connections are planned.

The following exchanges are planned

HTTP:
- GDAX (backend done)
- Bitfinex (backend done)
- Bitstamp (backend done)
- Kraken (backend done)
- Coincheck (backend done)
- OKCoin (backend done)
- BTC-E (backend done)
- Bittrex (backend done)

Websockets
- GDAX (planned)
- Bitstamp (planned)
- Bitfinex (planned)
- Poloniex (planned)

FIX
- GDAX (planned)
- ITBit (planned)


-`planned`: I'm currently designing base code for this exchange

-`backend done`: You're able to communicate with the API using the base class' functions

-`overlay funcs done`: I've added convenience methods which allow communication with the API, but not all arguments are integrated into the arguments list, and documenation may be missing.

-`fully implemented`: All API endpoints have a overlay method, which also features all applicable arguments as well as doc strings.

Additional clients will be added to (or removed from) this list, according to their liquidity and market volume.

In their basic form, clients provide a simple connection to APIs - that is, they handle authentication and request construction for you. As soon the above list is completed to a point where most of the exchanges are implemented (or whenever I feel like it), I will add convenience layers to the clients; this layer will aim to make calling the api feel more like a function, instead of string construction (i.e. `kraken.ticker('XBTEUR')`, instead of typing `kraken.public_query({'pair': 'XBTEUR'})`). 


# Output Format
All fully implemented `http` clients output Market data in the following format:

```
sent | received | Symbol | Exchange | Endpoint Timestamp | Type | Value
```
meaning that a request sent at 5am Jan 1st, 2016 for a BTCUSD bid order from an orderbook of layout {price, vol, timestamp}, ie {400, 0.4, 1451624340} from Kraken, and its answer received at 5:01am Jan 1st 2016 would look like this:
```
1451624400, 1451624460, XBTUSD, Kraken, 1451624340, Bid Price, 400
1451624400, 1451624460, XBTUSD, Kraken, 1451624340, Bid Vol, 0.4
```
If Endpoint timestamps arent available, `None` is returned in the `Endpoint Timestamp` instead.

Other Endpoints, such as `Balance` or `Fee` data, will be put out as is - the diversity of this output make it difficult to unify it under the above output. 

# Installation
`python3 setup.py install`


# Usage
Import any client from the `http` submodule.
```
from bitex.http import KrakenHTTP
uix = KrakenHTTP()
uix.orderbook('XBTEUR')
```

If you'd like to query a private endpoint, you'll have to either supply your secret & api keys like this:
```
uix = KrakenHTTP(key='your-api-key-here', secret='your-api-secret-here')
```

Or, which I'd recommend for safety and convenience reasons, pass a keyfile containing your api and secret on a seperate line each (Note: some clients require additional args to authenticate! These should come before the api and secret in the file!):
```
>my_api.key
513423534dljr1234  # Api key
knjer23053n90d02d3nd90d23d23d==  # Api Secret

>main.py
from bitex.http import KrakenHTTP
uix = KrakenHTTP(key_file='./my_api.key')
```






