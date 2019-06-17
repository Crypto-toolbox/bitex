# Third-party
import pluggy

# Home-brew
from bitex.plugins import base, specs


def get_plugin_manager():
    pm = pluggy.PluginManager("bitex")
    pm.add_hookspecs(specs)
    pm.load_setuptools_entrypoints("bitex")
    pm.register(base)
    return pm


pm = get_plugin_manager()

HOOKS = pm.hook

PLUGINS = {
    plugin_name: {"Auth": auth_class, "PreparedRequest": prep_class, "Response": resp_class}
    for plugin_name, auth_class, prep_class, resp_class in pm.hook.announce_plugin()
    if all(callable(cls) for cls in (auth_class, prep_class, resp_class))
}
