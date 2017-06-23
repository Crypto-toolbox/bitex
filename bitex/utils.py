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
