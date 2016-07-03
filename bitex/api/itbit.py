"""
Code based on ITBits RESTApi python module.
https://github.com/itbit/itbit-restapi-python
"""

import json
import time
import requests
import urllib.parse as urlparse

import base64
import hashlib
import hmac


#location of the api (change to https://beta-api.itbit.com/v1 for beta endpoint)
api_address = 'https://api.itbit.com/v1'


class MessageSigner:

    def make_message(self, verb, url, body, nonce, timestamp):
        # There should be no spaces after separators
        return json.dumps([verb, url, body, str(nonce), str(timestamp)], separators=(',', ':'))

    def sign_message(self, secret, verb, url, body, nonce, timestamp):
        message = self.make_message(verb, url, body, nonce, timestamp)
        sha256_hash = hashlib.sha256()
        nonced_message = str(nonce) + message
        sha256_hash.update(nonced_message.encode('utf8'))
        hash_digest = sha256_hash.digest()
        hmac_digest = hmac.new(secret, url.encode('utf8') + hash_digest, hashlib.sha512).digest()
        return base64.b64encode(hmac_digest)


class API:

    #clientKey, secret, and userId are provided by itBit and are specific to your user account
    def __init__(self, clientKey, secret, userId):
        self.clientKey = clientKey
        self.secret = secret.encode('utf-8')
        self.userId = userId
        self.nonce = 0

    def load_key(self, path):
        """Load key and secret from file.

        Argument:
        :param path: path to keyfile
        :type path: str

        """
        with open(path, 'r') as f:
            self.userId = f.readline().strip()
            self.clientKey = f.readline().strip()
            self.secret = f.readline().strip().encode('utf-8')

    def _query(self, verb, url, body_dict):
        url = api_address + url
        nonce = self._get_next_nonce()
        timestamp = self._get_timestamp()

        if verb in ("PUT", "POST"):
            json_body = json.dumps(body_dict)
        else:
            json_body = ""

        signer = MessageSigner()
        signature = signer.sign_message(self.secret, verb, url, json_body, nonce, timestamp)

        auth_headers = {
            'Authorization': self.clientKey + ':' + signature.decode('utf8'),
            'X-Auth-Timestamp': timestamp,
            'X-Auth-Nonce': nonce,
            'Content-Type': 'application/json'
        }

        return requests.request(verb, url, data=json_body, headers=auth_headers).json()

    #increases nonce so each request will have a unique nonce
    def _get_next_nonce(self):
        self.nonce += 1
        return self.nonce

    #timestamp must be unix time in milliseconds
    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _generate_query_string(self, filters):
        if filters:
            return '?' + urlparse.urlencode(filters)
        else:
            return ''