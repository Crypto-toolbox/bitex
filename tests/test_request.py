from unittest.mock import patch, MagicMock

import pytest

from bitex.request import BitexRequest, BitexPreparedRequest


class TestBitexRequest:

    @pytest.mark.parametrize(
        argnames="url, expected_target",
        argvalues=[
            ("https://google.com", None),
            ("http://google.com", None),
            ("google:something.com/else", "google")
        ],
        ids=['HTTPS Address', "HTTP Address", "Bitex Short-hand Address"]
    )
    def test_parse_target_exchange_parses_schemes_and_returns_correctly(
            self, url, expected_target):
        req = BitexRequest(url=url)
        # Assert the target exchange is parsed on __init__()
        assert req.exchange == expected_target

        # Assert the method itself returns correctly and the previously checked
        # attribute was not a default value.
        assert req.parse_target_exchange() == expected_target

    @patch("bitex.request.BitexPreparedRequest.prepare")
    def test_prepare_uses_custom_class_if_available(self, mock_prep_prepare):
        request = BitexRequest(url="test:instrument/ticker")
        custom_class = MagicMock(name="PseudoCustomClass")
        custom_class.return_value = custom_class
        assert request.exchange == "test"
        with patch.dict("bitex.request.PLUGINS", {"test": {"PreparedRequest": custom_class}}):
            assert request.prepare() == custom_class
        assert not mock_prep_prepare.called
        assert custom_class.called
        custom_class.assert_called_once_with("test")

    @patch("bitex.request.BitexPreparedRequest.prepare")
    def test_prepare_defaults_to_bitex_prepared_request_if_no_custom_class_is_available(self, _):
        request = BitexRequest(url="test:instrument/endpoint")
        assert isinstance(request.prepare(), BitexPreparedRequest)


class TestBitexPreparedRequest:
    def test_check_url_for_shorthand_successfully_parses_shorthands_without_an_action(self):
        url = "MyExchange:MyPair/ticker"
        result = BitexPreparedRequest.check_url_for_shorthand(url)
        assert result is not None
        assert result["exchange"] == "MyExchange"
        assert result["instrument"] == "MyPair"
        assert result["endpoint"] == "ticker"

    def test_check_url_for_shorthand_successfully_parses_shorthands_with_an_action(self):
        url = "MyExchange:MyPair/order/new"
        result = BitexPreparedRequest.check_url_for_shorthand(url)
        assert result is not None
        assert result["exchange"] == "MyExchange"
        assert result["instrument"] == "MyPair"
        assert result["endpoint"] == "order"
        assert result["action"] == "new"

    def test_check_url_for_shorthand_returns_none_if_the_shorthand_is_not_valid(self):
        url = "https://somehwere.com/123"
        result = BitexPreparedRequest.check_url_for_shorthand(url)
        assert result is None

