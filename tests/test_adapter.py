# Built-in
from unittest.mock import patch

# Third-party
import pytest

# Home-brew
from bitex.adapter import (
    BitexHTTPAdapter,
    BitexPreparedRequest,
    BitexResponse,
    CaseInsensitiveDict,
)


@pytest.fixture
def mock_url_response():
    """Simplistic urllib3.response.HTTPResponse Mock.

    Provides minimal set of attributes and values for these to construct a
    BitexResponse using :meth:`BitexHTTPAdaper.build_response`.
    """
    class MockResponse:
        def __init__(self):
            self.status = 200
            self.reason = "OK"
            self.headers = {"ACCESS": "Granted!"}

    return MockResponse()


@patch.dict("bitex.adapter.PLUGINS", {})
@patch("bitex.adapter.get_encoding_from_headers", return_value="UTF-512")
@patch("bitex.adapter.extract_cookies_to_jar")
def test_adapter_returns_bitex_response_by_default(mock_extract_cookies, mock_get_encoding, mock_url_response):
    request = BitexPreparedRequest("TestExchange")
    request.url = "http://bitex.com"

    adapter = BitexHTTPAdapter()
    bitex_response = adapter.build_response(request, mock_url_response)
    assert isinstance(bitex_response, BitexResponse)

    # Ensure method otherwise operates identically to the parent class's method.
    assert mock_extract_cookies.called
    assert mock_get_encoding.called
    assert bitex_response.encoding == "UTF-512"
    assert bitex_response.url == "http://bitex.com"
    assert bitex_response.status_code == 200
    assert bitex_response.reason == "OK"
    assert bitex_response.headers == CaseInsensitiveDict({"ACCESS": "Granted!"})
    assert bitex_response.raw == mock_url_response
    assert bitex_response.request == request
    assert bitex_response.connection == adapter
