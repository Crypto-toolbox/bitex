import pytest

from requests.sessions import cookielib
from requests.cookies import RequestsCookieJar
from unittest import mock
from unittest.mock import patch

from bitex.session import (
    BitexSession,
    BitexHTTPAdapter,
    BitexRequest,
    BitexResponse,
    BitexPreparedRequest,
)


def test_session_init_replaces_default_httpadapter_with_bitex_http_adapter_class():
    session = BitexSession()
    assert session.adapters['http://'] == BitexHTTPAdapter
    assert session.adapters['https://'] == BitexHTTPAdapter


@patch("bitex.session.BitexSession.send")
@patch("bitex.session.BitexSession.prepare_request")
@patch("bitex.session.BitexSession.merge_environment_settings")
class TestSessionRequestMethod:
    """Unit-test  the :meth:`BitexSession.request` method.

    The method mostly identical to the original :meth:`requests.Session.request`.
    We test that it calls all the same methods the original does, since we want
    to remain backwards-compatible to regular HTTP requests.

    All tests mock the following methods & classes::

        :cls:`BitexRequest`
        :meth:`BitexSession.send`
        :meth:`BitexSession.prepare_request`
        :meth:`BitexSession.merge_environment_settings`

    We mock these in order to avoid executing other code which may require
    valid input (and hence further mocking). It also means that for certain tests
    we do not need all of the mocked objects; hence, we store the unused mocks
    in throw-away variables (typically '_', '__', and so on). This makes it easier
    to distinguish the parts that are mocked *and* relevant to the current
    test function.
    """

    def setup_method(self):
        self.session = BitexSession()

    @patch("bitex.session.BitexRequest")
    def test_method_instantiates_a_bitex_request_instead_of_a_requests_Request(
            self, mock_request, _, __, ___):
        """Assert that :meth:`BitexSession` inits a :cls:`BitexRequest` when called."""
        self.session.request("GET", "http://test.com")
        mock_request.assert_called_once_with(
            method="GET", url="http://test.com",
            # Assert default values are propagated from method signature and
            # explicitly passed on to BitexRequest__init__ call.
            headers=None,
            files=None,
            data={},
            json=None,
            params={},
            auth=None,
            cookies=None,
            hooks=None,
            private=False,
        )

    def test_method_calls_sessions_prepare_request_method(
            self, _, mock_prep_request, __):

        class MethodCalled(AssertionError):
            pass

        def sentinel_exception(x):
            raise MethodCalled

        mock_prep_request.side_effect = sentinel_exception

        with pytest.raises(MethodCalled):
            self.session.request("GET", "http://test.com")

    def test_method_calls_merge_environment_settings_and_passes_params_on_correctly(
            self, mock_merge_env_settings, mock_prep_request, __):
        mock_merge_env_settings.return_value = {}
        given_url = "http://test.com"
        mock_prep_request.return_value = mock_prep_request
        mock_prep_request.url = given_url
        self.session.request(
            "GET", given_url, proxies='proxy', stream='stream', verify='verify', cert='MyCert'
        )
        mock_merge_env_settings.assert_called_once_with(given_url, 'proxy', 'stream', 'verify', 'MyCert')

    def test_method_calls_sessions_send_method_with_the_correct_arguments(
            self, _, mock_prep, mock_send):
        mock_prep.return_value = mock_prep
        self.session.request("GET", "http://test.com")
        mock_send.assert_called_once_with(
            mock_prep,
            # Assert default values are propagated from method signature and
            # passed on to BitexSession.prepare_request call.
            timeout=None,
            allow_redirects=True
        )


@patch("bitex.session.get_netrc_auth")
@patch("bitex.session.merge_setting")
@patch("bitex.session.merge_hooks")
@patch("bitex.session.merge_cookies")
@patch("bitex.session.cookiejar_from_dict")
@patch("bitex.session.RequestsCookieJar")
@patch("bitex.session.BitexPreparedRequest", autospec=BitexPreparedRequest)
class TestSessionPrepareRequestMethod:
    """Unit-test  the :meth:`BitexSession.request` method.

    As with :meth:`BitexSession.request`, this method is mostly an identical re-
    implementation of the parent class's :meth:`requests.Session.prepare_request`.

    In order to avoid unexpected behaviour, we must test meticulously all
    methods called in the parent's method are called in the re-implementation
    as well.

    Additionally, our custom code needs to be checked for as well, naturally.
    """

    def setup_method(self):
        self.session = BitexSession()

    def test_a_cookiejar_is_generated_from_cookies_kwarg_if_cookies_is_not_a_CookieJar_class_instance(
            self,
            _, __,
            mock_cookiejar_from_dict,
            ___, ____, _____, ______,
    ):
        """Assert the cookiejar is generated from kwargs if it isn't a CookieJar instance.

        The following is an excerpt of the code to be tested::

            if not isinstance(cookies, cookielib.CookieJar):
                cookies = cookiejar_from_dict(cookies)
        """
        mock_cookiejar_from_dict.reset_mock()
        req = BitexRequest(method="get", cookies={})
        self.session.prepare_request(req)
        assert mock_cookiejar_from_dict.called

    def test_a_cookiejar_is_NOT_generated_from_cookies_kwarg_if_cookies_is_a_CookieJar_class_instance(
            self,
            _, __,
            mock_cookiejar_from_dict,
            ___, ____, _____, ______,
    ):
        """Assert a cookiejar is *not* generated from kwargs if `cookies` *is* a CookieJar instance.

        The following is an excerpt of the code to be tested::

            if not isinstance(cookies, cookielib.CookieJar):
                cookies = cookiejar_from_dict(cookies)
        """
        mock_cookiejar_from_dict.reset_mock()

        # In order for our jar to not be replaced by an empty dict, we need to
        # populate it with a dummy value.
        jar = cookielib.CookieJar()
        jar._cookies = {'something': False}

        req = BitexRequest(method="get", cookies=jar)
        self.session.prepare_request(req)
        assert not mock_cookiejar_from_dict.called

    def test_merge_cookies_is_called_identically_to_the_original_implementation(
            self,
            _,
            mock_ReqCookieJar,
            mock_cookiejar_from_dict,
            mock_merge_cookies,
            __, ___, ____,
    ):
        """Assert that :func:`requests.session.merge_cookies` is called exactly twice.

        Furthermore, assert the first call's result is passed to the second
        instance of the call, like so::

            session_cookies = merge_cookies(RequestsCookieJar(), self.cookies)
            merged_cookies = merge_cookies(session_cookies, cookies)

        """
        given_cookies = {'hello': 'there'}
        mock_merge_cookies.return_value = mock_merge_cookies
        mock_cookiejar_from_dict.return_value = given_cookies
        req = BitexRequest(cookies=given_cookies)
        req.method = "get"
        self.session.prepare_request(req)

        mock_merge_cookies.has_calls(
            [
                mock.call(mock_merge_cookies, {'hello': 'there'}),
                mock.call(RequestsCookieJar(), self.session.cookies),
            ]
        )
        assert mock_merge_cookies.call_count == 2

    @pytest.mark.parametrize(
        "trust_env, kword_auth, instance_auth, expected_result",
        argvalues=[
            (True, True, True, False),
            (False, True, True, False),
            (True, False, True, False),
            (True, True, False, False),
            (False, False, True, False),
            (True, False, False, True),
            (False, True, False, False),
            (False, False, False, False),
        ]
    )
    def test_netrc_auth_is_fetched_identically_to_the_original_implementation(
            self,
            _, __, ___, ____, _____, ______,
            mock_get_netrc_auth,
            trust_env, kword_auth, instance_auth, expected_result,
    ):
        """The call to get_netrc_auth() is executed under the same conditions as before.

        This requires :attr:`BitexSession.trust_env` to be True, and authentication
        must be falsy in both the keyword arguments of :meth:`BitexSession.prepare_request`,
        as well as :attr:`BitexSession.auth`.

        If any of these conditions is *not* met, :func:`get_netrc_auth` should not be called.

        Code snippet to be tested::

            if not isinstance(cookies, cookielib.CookieJar):
                cookies = cookiejar_from_dict(cookies)
        """
        req = BitexRequest(auth=kword_auth)
        req.method = "get"
        self.session.auth = instance_auth
        self.session.trust_env = trust_env
        self.session.prepare_request(req)
        assert mock_get_netrc_auth.called == expected_result

    def test_prepare_request_calls_prepare_method_of_custom_bitex_prepared_request_class(
            self,
            mock_PreparedRequest,
            _,
            mock_cookiejar_from_dict,
            mock_merge_cookies,
            mock_merge_hooks,
            mock_merge_setting,
            __,
    ):
        """Ensure that we are actually preparing the request before returning it."""
        req = BitexRequest()
        req.method = "get"
        req.url = "http://test.com"
        req.files = "The file"
        mock_PreparedRequest.return_value = mock_PreparedRequest
        mock_merge_setting.return_value = mock_merge_setting
        mock_merge_hooks.return_value = mock_merge_hooks
        mock_merge_cookies.return_value = mock_merge_cookies
        assert isinstance(self.session.prepare_request(req), BitexPreparedRequest)
        mock_PreparedRequest.prepare.assert_called_once_with(
            method=req.method.upper(),
            url=req.url,
            files=req.files,
            data=req.data,
            json=req.json,
            headers=mock_merge_setting,
            params=mock_merge_setting,
            auth=mock_merge_setting,
            cookies=mock_merge_cookies,
            hooks=mock_merge_hooks,
        )

