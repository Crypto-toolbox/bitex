"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import time
import hashlib
import hmac
import base64
import json
import urllib.request, urllib.parse, urllib.error
import http.client

# Import Third-Party

# Import Homebrew


class Connection(object):
    """Kraken.com connection handler.

    """

    def __init__(self, uri='api.kraken.com', timeout=30):
        """ Create an object for reusable connections.

        :param uri: URI to connect to.
        :type uri: str
        :param timeout: blocking operations' timeout (in seconds).
        :type timeout: int
        :returns: TODO
        :raises: TODO

        """
        self.headers = {
            'User-Agent': 'krakenex/0.0.6 (+https://github.com/veox/python3-krakenex)'
        }
        self.conn = http.client.HTTPSConnection(uri, timeout=timeout)

    def close(self):
        """ Close the connection.

        """
        self.conn.close()

    def _request(self, url, req={}, headers={}):
        """ Send POST request to API server.

        :param url: fully-qualified URL with all necessary urlencoded
            information
        :type url: str
        :param req: additional API request parameters
        :type req: dict
        :param headers: additional HTTPS headers, such as API-Key and API-Sign
        :type headers: dict

        """
        data = urllib.parse.urlencode(req)
        headers.update(self.headers)

        self.conn.request("POST", url, data, headers)
        response = self.conn.getresponse()

        return response.read().decode()


class API(object):
    """Kraken.com cryptocurrency Exchange API.
    
    """
    def __init__(self, key = '', secret = '', conn = None):
        """Create an object with authentication information.
        
        :param key: key required to make queries to the API
        :type key: str
        :param secret: private key used to sign API messages
        :type secret: str
        :param conn: connection TODO
        :type conn: krakenex.Connection
        
        """
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.conn = conn


    def load_key(self, path):
        """Load key and secret from file.
        
        Argument:
        :param path: path to keyfile
        :type path: str
        
        """
        f = open(path, "r")
        self.key = f.readline().strip()
        self.secret = f.readline().strip()


    def set_connection(self, conn):
        """Set an existing connection to be used as a default in queries.

        :param conn: connection TODO
        :type conn: krakenex.Connection

        """
        self.conn = conn


    def _query(self, urlpath, req = {}, conn = None, headers = {}):
        """Low-level query handling.
        
        :param urlpath: API URL path sans host
        :type urlpath: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: connection TODO
        :type conn: krakenex.Connection
        :param headers: HTTPS headers
        :type headers: dict
        
        """
        url = self.uri + urlpath
        print(url, req)
        if conn is None:
            if self.conn is None:
                conn = Connection()
            else:
                conn = self.conn

        ret = conn._request(url, req, headers)
        return json.loads(ret)

    
    def query_public(self, method, req = {}, conn = None):
        """API queries that do not require a valid key/secret pair.
        
        :param method: API method name
        :type method: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: connection TODO
        :type conn: krakenex.Connection
        
        """
        urlpath = '/' + self.apiversion + '/public/' + method

        return self._query(urlpath, req, conn)

    
    def query_private(self, method, req={}, conn = None):
        """API queries that require a valid key/secret pair.
        
        :param method: API method name
        :type method: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: connection TODO
        :type conn: krakenex.Connection
        
        """
        urlpath = '/' + self.apiversion + '/private/' + method

        req['nonce'] = int(1000*time.time())
        postdata = urllib.parse.urlencode(req)

        # Unicode-objects must be encoded before hashing
        encoded = (str(req['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        headers = {
            'API-Key': self.key,
            'API-Sign': sigdigest.decode()
        }

        return self._query(urlpath, req, conn, headers)
