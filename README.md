# bitex
Bitex Crawler is a collection of API Clients for Crypto Currency Exchanges.

This project evolved out of the pure pleasure of writing clients for REST APIs, and a want and need for a single data stream to read from for my bitcoin bots. 

# What it do

As of now, only REST APIs are supported, implementations of websockets and FIX connections are planned.

The following exchanges are planned:

- GDAX (done)
- Bitfinex (done)
- Bitstamp (done)
- Kraken (done)
- Coincheck (done)
- OKCoin (done)
- BTC-E (planned)

Additional clients will be added to (or removed from) this list, according to their liquidity and market volume.

In their basic form, clients provide a simple connection to APIs - that is, they handle authentication and request construction for you. As soon the above list is completed to a point where most of the exchanges are implemented (or whenever I feel like it), I will add convenience layers to the clients; this layer will aim to make calling the api feel more like a function, instead of string construction (i.e. `kraken.ticker('XBTEUR')`, instead of typing `kraken.public_query({'pair': 'XBTEUR'})`). 

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


