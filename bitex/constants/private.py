# Built-in
import re

#: Regex to parse Shorthand urls for endpoints which do NOT support the `action`
#: option. An example of this would be::
#:
#:    kraken:BTCUSD/ticker
#
BITEX_SHORTHAND_NO_ACTION_REGEX = re.compile(
    r"(?P<exchange>.+):(?P<instrument>.+)/(?P<endpoint>(ticker|book|trades))"
)

#: Regex to parse Shorthand urls for endpoints which support the `action` option.
#: An example of this would be::
#:
#:    kraken:BTCUSD/order/new
#:
BITEX_SHORTHAND_WITH_ACTION_REGEX = re.compile(
    r"(?P<exchange>.+):(?P<instrument>.+)/(?P<endpoint>(wallet|order))/"
    r"(?P<action>(new|cancel|status|balance|withdraw|deposit))"
)
