# Import Third-Party
from requests import Response


class APIResponse(Response):
    __attrs__ = ['_content', 'status_code', 'headers', 'url', 'history',
                 'encoding', 'reason', 'cookies', 'elapsed', 'request',
                 '_formatted']

    def __init__(self, req_response, formatted_json=None):
        self._content = req_response._content
        self._content_consumed = req_response._content_consumed
        self.status_code = req_response.status_code
        self.headers = req_response.headers
        self.url = req_response.url
        self.history = req_response.history
        self.encoding = req_response.encoding
        self.reason = req_response.reason
        self.cookies = req_response.cookies
        self.elapsed = req_response.elapsed
        self.request = req_response.request
        self._formatted = formatted_json

    @property
    def formatted(self):
        return self._formatted

    @formatted.setter
    def formatted(self, val):
        self._formatted = val


if __name__ == '__main__':
    from bitex import Kraken

    k = Kraken()
    resp = k.ticker('XXBTZEUR')
    print(resp.formatted)
    print(resp.json())