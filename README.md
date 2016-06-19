# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

This project evolved out of the pure pleasure of writing clients for REST APIs, and a want and need for a single data stream to read from for my bitcoin bots. 

# What it do

As of now, only REST APIs are supported, implementations of websockets and FIX connections are planned.

The following exchanges are planned

HTTP:
- GDAX (done)
- Bitfinex (done)
- Bitstamp (done)
- Kraken (done)
- Coincheck (done)
- OKCoin (done)
- BTC-E (planned)


Additional clients will be added to (or removed from) this list, according to their liquidity and market volume.

In their basic form, clients provide a simple connection to APIs - that is, they handle authentication and request construction for you. As soon the above list is completed to a point where most of the exchanges are implemented (or whenever I feel like it), I will add convenience layers to the clients; this layer will aim to make calling the api feel more like a function, instead of string construction (i.e. `kraken.ticker('XBTEUR')`, instead of typing `kraken.public_query({'pair': 'XBTEUR'})`). 

You'll notice that clients relay data via udp socket; this is later caught by the postoffice module, which handles these formatted messages - for example allowing you to `subscribe` to various streams, save data from a particular set of clients to a file or send it out to a slack channel. 

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
As of now, there isn't a setup.py and its all mighty gritty and inconvenient; fear not, a fix for that is underway.

In the meantime, do your part of copy / pasting.

# Usage
Import any client from the `http` submodule.
```
from bitex.http import KrakenHTTP
uix = KrakenHTTP(('localhost', 676) # add any hostname / port combination you wish
uix.orderbook('XBTEUR')
```

If you'd like to query a private endpoint, you'll have to either supply your secret & api keys like this:
```
uix = KrakenHTTP(('localhost', 676), key='your-api-key-here', secret='your-api-secret-here')
```

Or, which I'd recommend for safety and convenience reasons, pass a keyfile containing your api and secret on a seperate line each (Note: some clients require additional args to authenticate! These should come before the api and secret in the file!):
```
>my_api.key
513423534dljr1234  # Api key
knjer23053n90d02d3nd90d23d23d==  # Api Secret

>main.py
from bitex.http import KrakenHTTP
uix = KrakenHTTP(('localhost', 676), key_file='./my_api.key')
```

# Credit
Most of the credit goes to Veox, who's `krakenex` module is the basis for almost all of the code for the http clients. If you like things a bit less shielded, i.e. don't mind packing payloads and defining endpoint yourself, you should check it out on his [github](https://github.com/veox/python3-krakenex)!


