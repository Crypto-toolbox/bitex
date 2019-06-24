import pytest

from bitex.exceptions import MissingPlugin


class TestMissingPluginException:

    def test_exception_message_is_constructed_as_expected(self):
        plugin_name = 'MyPlugin'
        expected_message = f"Missing plugin to handle requests for {plugin_name!r}!"
        with pytest.raises(MissingPlugin, match=expected_message):
            raise MissingPlugin(plugin_name)
