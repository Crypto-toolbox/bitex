# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


def kraken_formatter(base, quote):
    base = 'XBT' if base == 'BTC' else base
    quote = 'XBT' if base == 'BTC' else quote

    def add_prefix(cur):
        if cur in ('USD', 'EUR', 'GBP', 'JPY', 'CAD'):
            return 'Z' + cur
        else:
            return 'X' + cur

    return add_prefix(base) + add_prefix(quote)


def bitstamp_formatter(base, quote):
    return base.lower() + quote.lower()


def bitfinex_formatter(base, quote):
    base = 'DSH' if base == 'DASH' else base
    quote = 'DSH' if quote == 'DASH' else quote
    return base + quote


def bittrex_formatter(base, quote):
    return base + '-' + quote


def coincheck_formatter(base, quote):
    return base + quote


def gdax_formatter(base, quote):
    return base + '-' + quote


def itbit_formatter(base, quote):
    base = 'XBT' if base == 'BTC' else base
    quote = 'XBT' if base == 'BTC' else quote
    return base + quote


def okcoin_formatter(base, quote):
    return base.lower() + '_' + quote.lower()


def btce_formatter(base, quote):
    return base.lower() + '_' + quote.lower()


def ccex_formatter(base, quote):
    return base + '/' + quote


def cryptopia_formatter(base, quote):
    return base + '_' + quote


def gemini_formatter(base, quote):
    return base.lower() + quote.lower()


def yunbi_formatter(base, quote):
    return base.lower() + quote.lower()


def rocktrading_formatter(base, quote):
    return base + quote


def poloniex_formatter(base, quote):
    if ((quote == 'BTC') or (quote == 'USDT') or
            (quote == 'XMR' and not(base == 'BTC' or base == 'USDT'))):
        return quote + '_' + base
    else:
        return base + '_' + quote


def quoine_formatter(base, quote):
    return base + quote


def quadriga_formatter(base, quote):
    return base.lower() + '_' + quote.lower()


def hitbtc_formatter(base, quote):
    return base + quote


def vaultoro_formatter(base, quote):
    return base + '-' + quote


def bter_formatter(base, quote):
    return base.lower() + '_' + quote.lower()


formatters = {'Kraken': kraken_formatter, 'Bitstamp': bitstamp_formatter,
              'Bitfinex': bitfinex_formatter, 'Bittrex': bittrex_formatter,
              'CoinCheck': coincheck_formatter, 'GDAX': gdax_formatter,
              'ITBit': itbit_formatter, 'OKCoin': okcoin_formatter,
              'BTC-E': btce_formatter, 'C-CEX': ccex_formatter,
              'Cryptopia': cryptopia_formatter, 'Gemini': gemini_formatter,
              'The Rock Trading Ltd.': rocktrading_formatter,
              'Poloniex': poloniex_formatter, 'Quoine': quoine_formatter,
              'QuadrigaCX': quadriga_formatter, 'HitBTC': hitbtc_formatter,
              'Vaultoro': vaultoro_formatter, 'Bter': bter_formatter,
              'Yunbi': yunbi_formatter}


class PairFormatter:
    def __init__(self, base, quote):
        self._base = base
        self._quote = quote
        self._supported_by = []

    def __call__(self, *args, **kwargs):
        return self._base + self._quote

    def format(self, exchange_name):
        return formatters[exchange_name](self._base, self._quote)


