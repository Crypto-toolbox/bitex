"""Custom exceptions raised by the :mod:`bitex` code base."""


class MissingPlugin(ValueError):
    """A plugin was required to complete the request.

    :param str plugin_name: The name of the plugin which is missing.
    """

    def __init__(self, plugin_name: str, *args: list, **kwargs: dict) -> None:
        msg = f"Missing plugin to handle requests for {plugin_name!r}!"
        super(MissingPlugin, self).__init__(msg, *args, **kwargs)
