"""
Includes the base Class for crypto currency pairs, PairFormatter,
along with convencience wrappers for commonly used Pairs.

These can be imported to avoid typos by the user and passed to the APIs.

If the pair you want to query isn't present in here, creating such a pair is
simple enough - simply initialize the PairFormatter Class with the currencies
you want:

    my_pair = PairFormatter('BaseCurrency', 'QuoteCurrency')

This object now takes care of all formatting of any exchange, supported by
Bitex, you pass it to.
"""
# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


class PairFormatter:
    """Container Class which features formatting function for all supported
    exchanges. These Formatter functions apply any changes to make a given
    pair, pased as quote and base currency, compatible with an exchange.
    This does NOT include an availability check of the pair.
    It is therefore possible to format a given pair, even though it is not
    supported by the requested exchange.
    """
    def __init__(self, base, quote):
        self._base = base
        self._quote = quote
        self.formatters = {'Kraken':                self.kraken_formatter,
                           'Bitstamp':              self.bitstamp_formatter,
                           'Bitfinex':              self.bitfinex_formatter,
                           'Bittrex':               self.bittrex_formatter,
                           'CoinCheck':             self.coincheck_formatter,
                           'GDAX':                  self.gdax_formatter,
                           'ITBit':                 self.itbit_formatter,
                           'OKCoin':                self.okcoin_formatter,
                           'BTC-E':                 self.btce_formatter,
                           'C-CEX':                 self.ccex_formatter,
                           'Cryptopia':             self.cryptopia_formatter,
                           'Gemini':                self.gemini_formatter,
                           'The Rock Trading Ltd.': self.rocktrading_formatter,
                           'Poloniex':              self.poloniex_formatter,
                           'Quoine':                self.quoine_formatter,
                           'QuadrigaCX':            self.quadriga_formatter,
                           'HitBTC':                self.hitbtc_formatter,
                           'Vaultoro':              self.vaultoro_formatter,
                           'Bter':                  self.bter_formatter,
                           'Yunbi':                 self.yunbi_formatter}

    def __str__(self, *args, **kwargs):
        return self._base + self._quote

    def __call__(self):
        return self.__str__()

    def format_for(self, exchange_name):
        return self.formatters[exchange_name](self._base, self._quote)

    @staticmethod
    def kraken_formatter(base, quote):
        base = 'XBT' if base == 'BTC' else base
        quote = 'XBT' if quote == 'BTC' else quote

        def add_prefix(cur):
            if 'BCH' in (base, quote):
                return cur
            elif cur in ('USD', 'EUR', 'GBP', 'JPY', 'CAD'):
                    return 'Z' + cur
            else:
                return 'X' + cur

        return add_prefix(base) + add_prefix(quote)

    @staticmethod
    def bitstamp_formatter(base, quote):
        return base.lower() + quote.lower()

    @staticmethod
    def bitfinex_formatter(base, quote):
        base = 'DSH' if base == 'DASH' else base
        quote = 'DSH' if quote == 'DASH' else quote
        return base + quote

    @staticmethod
    def bittrex_formatter(base, quote):
        return quote + '-' + base

    @staticmethod
    def coincheck_formatter(base, quote):
        return base.lower() + '_' + quote.lower()

    @staticmethod
    def gdax_formatter(base, quote):
        return base + '-' + quote

    @staticmethod
    def itbit_formatter(base, quote):
        base = 'XBT' if base == 'BTC' else base
        quote = 'XBT' if base == 'BTC' else quote
        return base + quote

    @staticmethod
    def okcoin_formatter(base, quote):
        return base.lower() + '_' + quote.lower()

    @staticmethod
    def btce_formatter(base, quote):
        return base.lower() + '_' + quote.lower()

    @staticmethod
    def ccex_formatter(base, quote):
        return base.lower() + '-' + quote.lower()

    @staticmethod
    def cryptopia_formatter(base, quote):
        return base + '_' + quote

    @staticmethod
    def gemini_formatter(base, quote):
        return base.lower() + quote.lower()

    @staticmethod
    def yunbi_formatter(base, quote):
        return base.lower() + quote.lower()

    @staticmethod
    def rocktrading_formatter(base, quote):
        return base + quote

    @staticmethod
    def poloniex_formatter(base, quote):
        if ((quote == 'BTC') or (quote == 'USDT') or
                (quote == 'XMR' and not(base == 'BTC' or base == 'USDT'))):
            return quote + '_' + base
        else:
            return base + '_' + quote

    @staticmethod
    def quoine_formatter(base, quote):
        return base + quote

    @staticmethod
    def quadriga_formatter(base, quote):
        return base.lower() + '_' + quote.lower()

    @staticmethod
    def hitbtc_formatter(base, quote):
        return base + quote

    @staticmethod
    def vaultoro_formatter(base, quote):
        return base + '-' + quote

    @staticmethod
    def bter_formatter(base, quote):
        return base.lower() + '_' + quote.lower()


class BTCUSDFormatter(PairFormatter):
    def __init__(self):
        super(BTCUSDFormatter, self).__init__('BTC', 'USD')


class ETHUSDFormatter(PairFormatter):
    def __init__(self):
        super(ETHUSDFormatter, self).__init__('ETH', 'USD')


class XMRUSDFormatter(PairFormatter):
    def __init__(self):
        super(XMRUSDFormatter, self).__init__('XMR', 'USD')


class ETCUSDFormatter(PairFormatter):
    def __init__(self):
        super(ETCUSDFormatter, self).__init__('ETC', 'USD')


class ZECUSDFormatter(PairFormatter):
    def __init__(self):
        super(ZECUSDFormatter, self).__init__('ZEC', 'USD')


class DASHUSDFormatter(PairFormatter):
    def __init__(self):
        super(DASHUSDFormatter, self).__init__('DASH', 'USD')


class BCHUSDFormatter(PairFormatter):
    def __init__(self):
        super(BCHUSDFormatter, self).__init__('BCH', 'USD')


class ETHBTCFormatter(PairFormatter):
    def __init__(self):
        super(ETHBTCFormatter, self).__init__('ETH', 'BTC')


class LTCBTCFormatter(PairFormatter):
    def __init__(self):
        super(LTCBTCFormatter, self).__init__('LTC', 'BTC')


class XMRBTCFormatter(PairFormatter):
    def __init__(self):
        super(XMRBTCFormatter, self).__init__('XMR', 'BTC')


class ETCBTCFormatter(PairFormatter):
    def __init__(self):
        super(ETCBTCFormatter, self).__init__('ETC', 'BTC')


class ZECBTCFormatter(PairFormatter):
    def __init__(self):
        super(ZECBTCFormatter, self).__init__('ZEC', 'BTC')


class DASHBTCFormatter(PairFormatter):
    def __init__(self):
        super(DASHBTCFormatter, self).__init__('DASH', 'BTC')


class BCHBTCFormatter(PairFormatter):
    def __init__(self):
        super(BCHBTCFormatter, self).__init__('BCH', 'BTC')


BTCUSD = BTCUSDFormatter()
ETHUSD = ETHUSDFormatter()
XMRUSD = XMRUSDFormatter()
ETCUSD = ETCUSDFormatter()
ZECUSD = ZECUSDFormatter()
DASHUSD = DASHUSDFormatter()
BCHUSD = BCHUSDFormatter()

ETHBTC = ETHBTCFormatter()
LTCBTC = LTCBTCFormatter()
XMRBTC = XMRBTCFormatter()
ETCBTC = ETCBTCFormatter()
ZECBTC = ZECBTCFormatter()
DASHBTC = DASHBTCFormatter()
BCHBTC = BCHBTCFormatter()
