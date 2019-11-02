# Built-in
from unittest.mock import patch

# Third-party
import pytest

# Home-brew
from bitex.auth import BitexAuth
from bitex.request import BitexPreparedRequest


@pytest.fixture
def dummy_request():
    request = BitexPreparedRequest("TestExchange")
    request.url = "http://bitex.com"
    request.method = "GET"
    request.headers = {}
    return request


def test_key_as_bytes_property_encodes_key_to_bytes_using_utf8():
    auth = BitexAuth("key", "secret")

    assert auth.key_as_bytes == "key".encode("UTF-8")


def test_secret_as_bytes_property_encodes_secret_to_bytes_using_utf8():
    auth = BitexAuth("key", "secret")

    assert auth.secret_as_bytes == "secret".encode("UTF-8")


def test_call_method_does_nothing_by_default(dummy_request):
    auth = BitexAuth("key", "secret")

    assert auth(dummy_request) == dummy_request


def test_decode_body_returns_properly_decoded_body_as_object_if_its_json_encoded(dummy_request):
    json_data = {"foo": 1, "bar": 2}
    expected = (("bar", ["2"]), ("foo", ["1"]))

    dummy_request.headers["Content-Type"] = "application/json"
    dummy_request.prepare_body(None, None, json=json_data)

    assert BitexAuth.decode_body(dummy_request) == expected


def test_decode_body_returns_properly_decoded_body_as_sorted_list_of_tuples_if_its_not_json(dummy_request):
    data = {"foo": 1, "bar": 2}
    expected = (("bar", ["2"]), ("foo", ["1"]))

    dummy_request.prepare_body(data, None)

    assert BitexAuth.decode_body(dummy_request) == expected


@patch("bitex.auth.time.time", return_value=1000)
def test_nonce_method_returns_millisecond_resolution_as_str(mock_time):
    assert BitexAuth.nonce() == str(int(round(1000 * 1000)))
    assert mock_time.called
    assert mock_time.call_count == 1
