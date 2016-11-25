# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

It comes with two main parts - `bitex.api` represents the base level API
interfaces, on top of which the second part - `bitex.interfaces` - builds upon.
`bitex.api` classes can be used without making use of the interface classes.


# State
--------------------------------

**API** : **Completed**

**Interfaces** : **WIP**

--------------------------------


# Supported Exchanges

| Exchange       | API  | Authentication | Public Endpoints | Private Endpoints | Formatters | Tests |
|----------------|------|----------------|------------------|-------------------|------------|-------|
| Bitfinex       | Done | Done           | Done             | Done              | WIP        | WIP   |
| Bitstamp       | Done | Done           | Done             | Done              | WIP        | WIP   |
| Bittrex        | Done | Done           | Done             | Done              | WIP        | WIP   |
| C-Cex          | Done | BETA           | Done             | Done              | Planned    | WIP   |
| CoinCheck      | Done | Done           | Done             | Done              | Planned    | WIP   |
| Cryptopia      | Done | BETA           | Done             | Done              | Planned    | WIP   |
| GDAX           | Done | BETA           | Done             | Done              | Planned    | WIP   |
| Gemini         | Done | BETA           | Done             | Done              | Planned    | WIP   |
| itBit          | Done | BETA           | Done             | Done              | Planned    | WIP   |
| Kraken         | Done | Done           | Done             | Done              | WIP        | WIP   |
| OkCoin         | Done | BETA           | Done             | Done              | Planned    | WIP   |
| Poloniex       | Done | Done           | Done             | Done              | WIP        | WIP   |
| TheRockTrading | Done | BETA           | Done             | Done              | Planned    | WIP   |
| Yunbi          | Done | BETA           | Done             | Done              | Planned    | WIP   |


Additional clients will be added to (or removed from) this list, 
according to their liquidity and market volume.

# bitex.api

Classes found in `bitex.api` provide wrapper classes and methods for Python's
`requests` module, including handling of each exchange's specific authentication
procedure.

An example:
```
from bitex.api.rest import KrakenREST

k = KrakenREST()
k.load_key('kraken.key')  # loads key and secret from given file;

# Query a public endpoint
k.query('GET','public/Depth', params={'pair': 'XXBTZUSD'})

# Query a private (authenticated endpoint)
q = {'pair': 'XXBTZUSD', 'type': 'sell', 'ordertype': 'limit', 'price': 1000.0,
     'volume': 0.01, 'validate': True}
k.query('POST','private/AddOrder', authenticate=True, params=q)

```

Example `.key` file:
```
>>>dummy.key
my_api_key
my_fancy_api_secret
```

If the api requires further details, for example a userid or account 
number (for example for bitstamp), you should check the class method's doc string,
although usually this information needs to go before the api key
and secret, on a separate line each.
```
>>>dummy2.key
Userid
accountname
my_api_key
my_fancy_api_secret
```

# bitex.interfaces

Built on top of `bitex.api`'s api classes are the slightly more sophisticated
exchange interfaces in `bitex.interfaces`. These have been written to unify
the diverse REST APIs of the implemented exchanges, by providing the same methods and method parameters
across all of them.

For example, querying tickers looks the same on all exchanges, as well as
placing an order, using `bitex.interface`:

```
from bitex import Kraken, Bitstamp, Gemini
k = Kraken(key_file='krkn.key')
b = Bitstamp(key_file='btst.key')
g = Gemini(key_file='gmni.key')

k.ticker('XBTUSD')
b.ticker('btceur')
g.ticker('BTC-USD')

k.ask(pair, price, size)
b.ask(pair, price, size)
g.ask(pair, price, size)
```


# Installation
`python3 setup.py install`

or via pip

`pip install BitEx`









