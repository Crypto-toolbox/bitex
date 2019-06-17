"""A customized version of :cls:``requests.Session``, tailored to the :mod:``bitex`` library."""
# Built-in
import logging
import platform
import time

# Third-party
import requests
from requests.compat import cookielib
from requests.cookies import RequestsCookieJar, cookiejar_from_dict, merge_cookies
from requests.sessions import merge_hooks, merge_setting
from requests.structures import CaseInsensitiveDict
from requests.utils import get_netrc_auth

# Home-brew
from bitex.adapter import BitexHTTPAdapter
from bitex.plugins import PLUGINS
from bitex.request import BitexPreparedRequest, BitexRequest
from bitex.response import BitexResponse

# Preferred clock, based on which one is more accurate on a given system.
if platform.system() == "Windows":
    try:  # Python 3.3+
        preferred_clock = time.perf_counter
    except AttributeError:  # Earlier than Python 3.
        preferred_clock = time.clock
else:
    preferred_clock = time.time


# Init Logging Facilities
log = logging.getLogger(__name__)


class BitexSession(requests.Session):
    """Custom requests.Session object for keep-alive http connections to API endpoints.

    It expects a BitexAuth instance or subclass thereof on instantiation, and
    assigns it as the default authentication object for any requests made via
    this class's instance.

    :mod:`bitex` uses short-hands to unify urls and make using plugins easier.
    All methods implemented in this class support these shortened urls::

        <exchange>:<instrument>/<endpoint>/<action>

    `exchange` refers to the exchange you want to request data from.
    `instrument` is either a single `currency` or a currency `pair`.
    `endpoint` describes the kind of endpoint you'd like to use:

        - `trades`
        - `book`
        - `ticker`
        - `wallet`
        . `order`

    The latter two endpoint types support `actions`, which are listed below:

        - `wallet` actions:

            - `deposit`
            - `withdraw`
            - `balance`

        - `order` actions:

            - `new`
            - `status`
            - `cancel`

    Using one of these methods requires an adequate plugin to be installed for
    `exchange`. If no such plugin is present, an :exc:`MissingPlugin` exception
    is raised by :cls:`bitex.abc.request.BitexPreparedRequest`.

    Using this shorthand is not mandatory. You may as well construct the entire
    url of an endpoint you'd like to reach manually, and :mod:`bitex` will do the
    right thing.
    """

    def __init__(self) -> None:
        super(BitexSession, self).__init__()
        self.adapters["http://"] = BitexHTTPAdapter
        self.adapters["https://"] = BitexHTTPAdapter

    def request(
        self,
        method,
        url,
        private=False,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> BitexResponse:
        """Construct a :cls:`BitexRequest`, prepare and send it.

        `url` may either be a URL starting with http/https, or a :mod:`bitex`
        short-hand url in the format of `<exchange>:<instrument>/<data>/<action>`.
        """
        # Create the Request.
        req = BitexRequest(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            private=private,
        )
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(prep.url, proxies, stream, verify, cert)

        # Send the request.
        send_kwargs = {"timeout": timeout, "allow_redirects": allow_redirects}
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)

        return resp

    def prepare_request(self, request: BitexRequest) -> BitexPreparedRequest:
        """Prepare a :cls:`BitexPreparedRequest` object for transmission.

        This implementation extends :cls:`requests.Session.prepare_request` by
        making a call to :var:`bitex.PLUGINS` and checking if we have any plugins
        that may provide a custom :cls:`BitexPreparedRequest` class.
        """
        cookies = request.cookies or {}

        # Bootstrap CookieJar.
        if not isinstance(cookies, cookielib.CookieJar):
            cookies = cookiejar_from_dict(cookies)

        # Merge with session cookies
        session_cookies = merge_cookies(RequestsCookieJar(), self.cookies)
        merged_cookies = merge_cookies(session_cookies, cookies)

        # Set environment's basic authentication if not explicitly set.
        auth = request.auth
        if self.trust_env and not auth and not self.auth:
            auth = get_netrc_auth(request.url)

        # Inject any custom classes for handling the exchange stated in the
        # BitexRequest object.
        custom_classes = PLUGINS.get(request.exchange, None)
        if custom_classes:
            p = custom_classes["PreparedRequest"](request.exchange)
            # Only use the custom auth class if no auth object was
            # provided explicitly. Otherwise we would overwrite user-specified
            # auth objects passed to self.request.
            if not self.auth and request.private:
                self.auth = custom_classes["Auth"](self.key, self.secret)
        else:
            p = BitexPreparedRequest(request.exchange)
        p.prepare(
            method=request.method.upper(),
            url=request.url,
            files=request.files,
            data=request.data,
            json=request.json,
            headers=merge_setting(request.headers, self.headers, dict_class=CaseInsensitiveDict),
            params=merge_setting(request.params, self.params),
            auth=merge_setting(auth, self.auth),
            cookies=merged_cookies,
            hooks=merge_hooks(request.hooks, self.hooks),
        )
        return p

    @property
    def key(self) -> str:
        """Return the Auth's key attribute value.

        :rtype: str
        """
        return self.auth.key

    @key.setter
    def key(self, value: str):
        """Set the Auth's key attribute value.

        :type value: str
        """
        self.auth.key = value

    @property
    def secret(self) -> str:
        """Return the Auth's secret attribute value.

        :rtype: str
        """
        return self.auth.secret

    @secret.setter
    def secret(self, value: str):
        """Set the Auth's secret attribute value.

        :type value: str
        """
        self.auth.secret = value

    def ticker(self, exchange: str, pair: str, method: str = "GET", **kwargs) -> BitexResponse:
        """Request ticker data for the given `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str pair: The currency pair to request data for.
        :param str method:
            The HTTP method to use when requesting the data. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        """
        return self.request(method, f"{exchange}:/{pair}/ticker", **kwargs)

    def orderbook(self, exchange: str, pair: str, method: str = "GET", **kwargs) -> BitexResponse:
        """Request order book data for the given `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str pair: The currency pair to request data for.
        :param str method:
            The HTTP method to use when requesting the data. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        """
        return self.request(method, f"{exchange}:/{pair}/book", **kwargs)

    def trades(self, exchange: str, pair: str, method: str = "GET", **kwargs) -> BitexResponse:
        """Request trade data for the given `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str pair: The currency pair to request data for.
        :param str method:
            The HTTP method to use when requesting the data. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        """
        return self.request(method, f"{exchange}:/{pair}/trades", **kwargs)

    def new_order(self, exchange: str, pair: str, method: str = "POST", **kwargs) -> BitexResponse:
        """Create a new order for `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str pair: The currency pair to place the order for.
        :param str method:
            The HTTP method to use when placing the order. This defaults to POST.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        :rtype: BitexResponse

        ..Note::

            Note that negative `size` values (-5, "-33", etc) result in ask
            orders, positive sizes result in a bid order.
        """
        return self.request(method, f"{exchange}:/{pair}/order/new", **kwargs)

    def cancel_order(
        self, exchange: str, pair: str, method: str = "DELETE", **kwargs
    ) -> BitexResponse:
        """Cancel an order with the given `order_id` for `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str pair: The currency pair to place the order for.
        :param order_id: The order id of the order you'd like to cancel.
        :param str method:
            The HTTP method to use when placing the order. This defaults to DELETE.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        :rtype: BitexResponse
        """
        return self.request(method, f"{exchange}:/{pair}/order/cancel", **kwargs)

    def order_status(
        self, exchange: str, pair: str, method: str = "GET", **kwargs
    ) -> BitexResponse:
        """Request the order status for `order_id` and `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str pair: The currency pair to place the order for.
        :param str method:
            The HTTP method to use when placing the order. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        :rtype: BitexResponse
        """
        return self.request(method, f"{exchange}:/{pair}/order/status", **kwargs)

    def wallet(self, exchange: str, currency: str, method: str = "GET", **kwargs) -> BitexResponse:
        """Request wallet data for the given `pair` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str currency: The currency to request data for.
        :param str method:
            The HTTP method to use when requesting the data. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        """
        return self.request(method, f"{exchange}:/{currency}/wallet", **kwargs)

    def withdraw(
        self, exchange: str, currency: str, amount: str, method: str = "PUT", **kwargs
    ) -> BitexResponse:
        """Request a withdrawal of the given `currency` at the given `exchange`.

        :param str exchange: The exchange you'd like to request data from.
        :param str currency: The currency to withdraw.
        :param str amount: The amount to withdraw.
        :param str method:
            The HTTP method to use when requesting the data. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        """
        return self.request(
            method, f"{exchange}:/{currency}/wallet/withdraw?amount={amount}", **kwargs
        )

    def deposit(
        self, exchange: str, currency: str, method: str = "GET", **kwargs
    ) -> BitexResponse:
        """Request the deposit address of the given `currency`'s wallet.

        :param str exchange: The exchange you'd like to request data from.
        :param str currency: The currency to withdraw.
        :param str method:
            The HTTP method to use when requesting the data. This defaults to GET.
        :param Any kwargs:
            Additional keyword arguments which are passed on to
            :meth:`requests.Session.request`.
        """
        return self.request(method, f"{exchange}:/{currency}/wallet/deposit", **kwargs)
