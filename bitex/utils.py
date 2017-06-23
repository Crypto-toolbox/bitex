from functools import wraps

@wraps
def check_bitfinex_version_compatibility(func, *args, **kwargs):
    v2_endpoints = ['wallets', 'orders', 'order_trades', 'positions',
                    'offers', 'funding_info', 'performance', 'alert_list',
                    'alert_set', 'alert_delete', 'calc_available_balance',
                    'market_average_price', 'candles', 'ticker', 'tickers']
    def wrapper(*args, **kwargs):
        if func.__name__ in v2_endpoints and args[0].api.version != 'v2':
            raise UnsupportedEndpointError('This endpoint is only available for'
                                           'api version v2 (current is %s)'
                                           % self.api.version)
        elif func.__name__ not in v2_endpoints and args[0].api.version == 'v2':
            raise UnsupportedEndpointError('This endpoint is only available for'
                                           'api version v1 (current is %s)'
                                           % self.api.version)
        else:
            return func(*args, **kwargs)
    return wrapper

@wraps
def check_compatibility(**version_func_pairs):
    """This Decorator maker takes any number of
    version_num=[list of compatible funcs] pairs, and checks if the
    decorated function is compatible with the currently set API version.
    Should this not be the case, an UnsupportedEndpointError is raised.
    """
    method_compatibility = {}
    for k in version_func_pairs:
        d = {value: k for value in version_func_pairs[k]}
        method_compatibility.update(d)

    def decorator(func):
        def wrapped(*args, **kwargs):
            interface = args[0]
            if method_compatibility[func.__name__] != interface.api.version:
                raise UnsupportedEndpointError("Method not available on this API"
                                               "version (current is %s, "
                                               "supported is %s)" %
                                               (interface.api.version,
                                                method_compatibility[func.__name__]))
            return func(*args, **kwargs)
        return wrapped
    return decorator
