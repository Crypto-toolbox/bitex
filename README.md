# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

It comes with two parts - `bitex.api` represents the base level API
interfaces, on top of which the second part - `bitex.interfaces` - builds upon.
`bitex.api` classes can be used without making use of the interface classes.


# State
--------------------------------

**API** : **Completed**

**Interfaces** : **WIP**

--------------------------------


# Supported Exchanges

| Exchange       | API  | Authentication | Public Endpoints*[^1] | Private Endpoints[^1] | Formatters | Tests |
|----------------|------|----------------|-------------------|--------------------|------------|-------|
| Bitfinex       | Done | Done           | Done              | Done               | WIP        | WIP   |
| Bitstamp       | Done | Done           | Done              | Done               | WIP        | WIP   |
| Bittrex        | Done | Done           | Done              | Done               | WIP        | WIP   |
| C-Cex          | Done | BETA           | Done              | Done               | WIP        | WIP   |
| CoinCheck      | Done | Done           | Done              | Done               | WIP        | WIP   |
| Cryptopia      | Done | BETA           | Done              | Done               | WIP        | WIP   |
| GDAX           | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Gemini         | Done | BETA           | Done              | Done               | WIP        | WIP   |
| itBit          | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Kraken         | Done | Done           | Done              | Done               | WIP        | WIP   |
| OkCoin         | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Poloniex       | Done | Done           | Done              | Done               | WIP        | WIP   |
| TheRockTrading | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Yunbi          | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Quoine         | Done | BETA           | Done              | Done               | WIP        | WIP   |
| QuadrigaCX     | Done | BETA           | Done              | Done               | WIP        | WIP   |

Additional clients will be added to (or removed from) this list, 
according to their liquidity and market volume.

[^1]: This table considers standardized methods only, when describing the state. See section `Standardized Methods` for more

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

# Query a private (authenticated) endpoint
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
although usually this information needs to go after the api key
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
across all of them (see next section, `Standardized Methods`, for more information).

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
# bitex.formatters

This module provide formatters for the standardized methods, formatting their json output into a uniform layout. They are a work in progress feature.

Be mindful that, in order to provide a unified output format, some fields have been dropped in the formatted output! If you rely on one of these dropped fields, be sure to use the returned `requests.response()` object, and parse the json yourself:

```
from bitex import Kraken
k = Kraken()
formatted_output, requests_response_object = k.ticker()
print(formatted_output)  # drops bid/ask sizes, vwap and other data
print(requests.response_object.json())  # Returns all data
```

The following is a table of all formatters currently implemented - any method not marked as `Done` will not do any formatting, and simply return `requests.response.json()` if data contains valid json - else `None` is returned instead.

| Exchange          | `ticker()` | order_book() | trades() | bid()/ask() | order() | cancel_order() | balance() | withdraw() | deposit() |
|-------------------|------------|--------------|----------|-------------|---------|----------------|-----------|------------|-----------|
| Bitfinex          | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Bitstamp          | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Bittrex           | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| C-Cex             | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Coincheck         | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Cryptopia         | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| GDAX              | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Gemini            | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| itBit             | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Kraken            | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| OKCoin            | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Poloniex          | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| QuadrigaCX        | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Quoine            | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| TheRockTradingLTD | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Yunbi             | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |

# Standardzied Methods

As explained in the previous section, __standardized methods__ refer to the methods of each interface,
which have been deemed as part of the set of minimal methods and functions required, to trade
at an exchange via its API. They feature the following characteristics:

- Each method has an identical method header across all interfaces
- Its output is identical across all interfaces

# Installation

Manually, using the supplied `setup.py` file:

`python3 setup.py install`

or via pip

`pip install BitEx`

