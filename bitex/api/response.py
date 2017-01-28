# Import Third-Party
from requests import Response


class APIResponse(Response):
    __attrs__ = ['_content', 'status_code', 'headers', 'url', 'history',
                 'encoding', 'reason', 'cookies', 'elapsed', 'request',
                 '_formatted']

    def __init__(self, formatted_json, req_response):
        self._content = req_response._content
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

if __name__ == '__main__':
    from bitex import Kraken
    k = Kraken()
    _, resp = k.ticker('XXBTZEUR')
    x = APIResponse(_, resp)
    print(x())
    print(x.json())