# BitEx
BitEx is a collection of API Clients for Crypto Currency Exchanges.

It comes with two parts - `bitex.api` represents the base level API
interfaces, on top of which the second part - `bitex.interfaces` - builds upon.
`bitex.api` classes can be used without making use of the interface classes.

Donations welcome!
BTC @ 3D4yuyf84eQUauyZLoQKyouPuThoxMMRZa
# State
--------------------------------

**RESTAPI** : **Completed**

**Interfaces** : **WIP**

--------------------------------


# Supported Exchanges

| Exchange             | REST  API | Authentication | Public Interface<sup>1</sup> | Private Interface<sup>1</sup> | Tests             |
|----------------------|-----------|----------------|------------------|-------------------|-------------------|
| Bitfinex             | DONE      | DONE           | DONE             | DONE              | Passing           |
| Bitstamp             | DONE      | DONE           | DONE             | DONE              | Passing           |
| Bittrex              | DONE      | DONE           | DONE             | DONE              | Passing           |
| BTCE                 | DONE      | DONE           | DONE             | DONE              | Passing           |
| Bter                 | DONE      | DONE           | DONE             | DONE              | Passing           |
| C-CEX                | DONE      | DONE           | DONE             | DONE              | Passing           |
| CoinCheck            | DONE      | DONE           | DONE             | DONE              | Passing           |
| Cryptopia            | DONE      | DONE           | DONE             | DONE              | Passing           |
| HitBTC               | DONE      | DONE           | DONE             | DONE              | Passing           |
| Kraken               | DONE      | DONE           | DONE             | DONE              | Passing           |
| OKCoin               | DONE      | DONE           | DONE             | DONE              | Passing           |
| Poloniex             | DONE      | DONE           | DONE             | DONE              | Passing           |
| QuadrigaCX           | DONE      | DONE           | DONE             | DONE              | Passing           |
| The Rock Trading LTD | DONE      | DONE           | DONE             | DONE              | Partially Passing |
| Vaultoro             | DONE      | DONE           | DONE             | DONE              | Failing           |


Additional clients will be added to (or removed from) this list, 
according to their liquidity and market volume.

_<sup>1</sup>): This table considers standardized methods only, when describing the state. 
See section `Standardized Methods` for more information on these._


# Standardized Methods

As explained in the previous section, __standardized methods__ refer to the methods of each interface
which have been deemed as part of the set of minimal methods and functions required to trade
at an exchange via its API.

The Methods are:

| Method           | Required Parameters | Requires Authentification? | Function                                                                                        |
|------------------|---------------------|----------------------------|-------------------------------------------------------------------------------------------------|
| ticker()         | pair                | No                         | Returns a specified pair's 'ticker' data from the exchange API.                                 |
| order_book       | pair                | No                         | Returns a specified pair's `order book` data from the exchange API.                             |
| `trades()`       | pair                | No                         | Returns a specified pair's `trades` data from the exchange API                                  |
| `ask()`          | pair, price, size   | Yes                        | Places an `ask` order of type `limit` via the exchange API.                                     |
| `bid()`          | pair, price, size   | Yes                        | Places an `bid` order of type `limit` via the exchange API.                                     |
| `order_status()` | order_id            | Yes                        | Requests the status of the given `order id` via the exchange API.                               |
| `open_orders()`  | -                   | Yes                        | Requests all `open orders` via the exchange API.                                                |
| `cancel_order()` | *order_ids          | Yes                        | Cancels one or more `orders` by their given `order id` via the exchange API.                    |
| `wallet()`       | -                   | Yes                        | Requests the current balances of the account associated with the API keys via the exchange API. |


# Standardized Pairs

`Bitex` comes with a `PairFormatter()` class, which formats a given symbol
 pair into a format which is recognized by the exchange you're querying.
 
 This allows you to specify a pair once, without having to worry about
 whether or not you typed it correctly for each individual exchange.
 
 An example:
 
 The Pair `ETHBTC` is denoted as follows:
  - At Kraken it goes by XETHXXBT
  - At Poloniex it goes by BTC_ETH
  - At Bittrex it goes by BTC-ETH
  - at OKCoin it goes by btc_eth
 
 Instead of passing a string to the standardized methods, then, you may
 pass a `PairFormatter()` object instead.
 It automatically formats the pair accordingly when a standardized method 
 is invoked.
 
 You can create a custom `PairFormatter()` easily. Let's consider two 
 imaginary crypt currencies, Bla-Coin(BLA) and Fake-Coin (FKE): 
 
```
    from bitex.pairs import PairFormatter
    
    class BLAFKE(PairFormatter):
        def __init__(self):
            super(MySpecialPairFormatter).__init__(base='BLA', quote='FKE')
```

And that's all you need to do! Whenever you pass this to a standardized
method, the method will call the `PairFormatter()`'s `format_for()` method,
and let it take care of the formatting:

```
    >>>BLAFKE.format_for('Kraken')
    'XBLAXFKE'
    >>>BLAFKE.format_for('Bittrex')
    'BLA-FKE'
```



# Installation

Manually, using the supplied `setup.py` file:

`python3 setup.py install`

or via pip

`pip install BitEx`

