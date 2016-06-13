# bitex-crawler
Bitex Crawler is a collection of API Clients for Crypto Currency Exchanges.

This project evolved out of the pure pleasure of writing clients for REST APIs, and a want and need for a single data stream to read from for my bitcoin bots. 

# What it do

As of now, only REST APIs are supported, implementations of websockets and FIX connections are planned.

The following exchanges are planned:

- GDAX (in progress)
- Bitfinex (done)
- Bitstamp (done)
- Kraken (done)
- Coincheck (done)
- OKCoin (planned)
- BTC-E (planned)

Additional clients will be added to (or removed from) this list, according to their liquidity and market volume.

In their basic form, clients provide a simple connection to APIs - that is, they handle authentication and request construction for you. As soon the above list is completed to a point where most of the exchanges are implemented (or whenever I feel like it), I will add convenience layers to the clients; this layer will aim to make calling the api feel more like a function, instead of string construction (i.e. `kraken.ticker('XBTEUR')`, instead of typing `kraken.public_query({'pair': 'XBTEUR'})`). 

Additionally, I'll work on implementing a node launcher - a threaded udp server which launches and supervises each client, taking their queried data and bundling it into a single, unified data layout - allowing you to do whatever you want with that.

# Credit
Most of the backend credit goes to Veox, who's krakenex module is the basis for almost all of the code for the http clients. I've merely adjusted for some minor differences, also dropping the `http module` for the `requests` module.


