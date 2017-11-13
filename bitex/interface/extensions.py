# Import Built-Ins
import logging
import time

# Import Third-Party
import requests

# Import Homebrew
from bitex.exceptions import UnsupportedPairError

from bitex.api.REST.bitfinex import BitfinexREST
from bitex.api.REST.bitstamp import BitstampREST
from bitex.api.REST.bittrex import BittrexREST
from bitex.api.REST.bter import BterREST
from bitex.api.REST.ccex import CCEXREST
from bitex.api.REST.coincheck import CoincheckREST
from bitex.api.REST.cryptopia import CryptopiaREST
from bitex.api.REST.gdax import GDAXREST
from bitex.api.REST.gemini import GeminiREST
from bitex.api.REST.hitbtc import HitBTCREST
from bitex.api.REST.itbit import ITbitREST
from bitex.api.REST.kraken import KrakenREST
from bitex.api.REST.okcoin import OKCoinREST
from bitex.api.REST.poloniex import PoloniexREST
from bitex.api.REST.quadriga import QuadrigaCXREST
from bitex.api.REST.quoine import QuoineREST
from bitex.api.REST.rocktrading import RockTradingREST
from bitex.api.REST.vaultoro import VaultoroREST
from bitex.api.REST.yunbi import YunbiREST

from bitex.interface.rest import RESTInterface
from bitex.utils import check_version_compatibility, check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)

