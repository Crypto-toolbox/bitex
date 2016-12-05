"""
Parses and formats JSON Data returned by bitex.api calls.

ticker(data):
    Returns bid, ask, and 24h volume
    ex.:
        ['0.014', '0.015', '15.5', *other_data]

order_book(data):
    Returns dict of lists of lists of quotes in format [ts, price, size]
    ex.:
        {'bids': [['1480941692', '0.014', '10'],
                  ['1480941690', '0.013', '0.66'],
                  ['1480941688', '0.012', '3']],
         'asks': [['1480941691', '0.015', '1'],
                  ['1480941650', '0.016', '0.67'],
                  ['1480941678', '0.017', '23']]}

trades(data):
    Returns list of trades in format [ts, price, size, side]
    ex.:
        [['1480941692', '0.014', '10', 'sell'], ['1480941690', '0.013', '0.66', 'buy'],
         ['1480941688', '0.012', '3', 'buy']]

bid / ask(data):
    Returns the order id as str if successful, else False

order_status(data):
    Returns True if it exists, False if it doesn't exist

cancel(data):
    returns True if it was cancelled successfully, else False

balance(data):
    Returns dict of available balances, with currency names as keys - this ignores
    any amount already involved in a trade (i.e. margin)
    ex.:
        {'BTC': '12.04', 'LTC': '444.12'}

withdraw(data):
    Returns a list giving details of success and transaction details, or failure
    and reason thererof
    ex.:
        [True, currency, amount, target_address, txid]
        [False, 'Reason for failure/ error message']

deposit_address(data):
    Returns deposit address as str
"""

# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew

log = logging.getLogger(__name__)


def trade(data, *args, **kwargs):
    if not data['error']:
        return data['result']['txid']
    else:
        return False


def order_book(data, *args, **kwargs):
    pair = args[1]
    forex = ['EUR', 'USD', 'GBP', 'JPY', 'CAD']
    if len(pair) == 6:
        base_cur = pair[:3]
        quote_cur = pair[3:]
        if base_cur.upper() in forex:
            base_cur = 'Z' + base_cur
        else:
            base_cur = 'X' + base_cur

        if quote_cur.upper() in forex:
            quote_cur = 'Z' + quote_cur
        else:
            quote_cur = 'X' + quote_cur
        return data['result'][base_cur+quote_cur]
    else:
        return data['result'][pair]


def cancel(data, *args, **kwargs):
    if int(data['result']['count']) == 1:
        return True
    else:
        return False
