# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

"""
import json
from datetime import datetime

class env_type(object):
    def __init__(self, config_id, web_endpoint, api_endpoint):
        self.config_id = config_id
        self.web_endpoint = web_endpoint
        self.api_endpoint = api_endpoint
    
class environment(object):
    PRODUCTION = env_type("api.ebay.com", "https://auth.ebay.com/oauth2/authorize", "https://api.ebay.com/identity/v1/oauth2/token")
    SANDBOX = env_type("api.sandbox.ebay.com", "https://auth.sandbox.ebay.com/oauth2/authorize", "https://api.sandbox.ebay.com/identity/v1/oauth2/token")


class credentials(object):
    def __init__(self, client_id, client_secret, dev_id, ru_name):
        self.client_id = client_id 
        self.dev_id = dev_id
        self.client_secret = client_secret
        self.ru_name = ru_name
    

class oAuth_token(object):

    def __init__(self, error=None, access_token=None, refresh_token=None, refresh_token_expiry=None, token_expiry=None):
        '''
            token_expiry: datetime in UTC
            refresh_token_expiry: datetime in UTC
        '''
        self.access_token = access_token if access_token else None
        self.token_expiry = datetime.fromtimestamp(token_expiry) if token_expiry else None
        self.refresh_token = refresh_token if refresh_token else None
        self.refresh_token_expiry = datetime.fromtimestamp(refresh_token_expiry) if refresh_token_expiry else None
        self.error = error if error else None

    def to_dict(self, epoch=False):
        d = {}

        if self.error != None:
            d["error"]: self.error

        if self.access_token != None:
            d["access_token"] = self.access_token
            if epoch:
                d["expires_in"] = self.token_expiry.timestamp()
            else:
                d["expires_in"] = self.token_expiry.strftime('%Y-%m-%dT%H:%M:%S:%f')
 
        if self.refresh_token != None:
            d["refresh_token"] = self.refresh_token
            if epoch:
                d["refresh_token_expire_in"] = self.refresh_token_expiry.timestamp()
            else:
                d["refresh_token_expire_in"] = self.refresh_token_expiry.strftime('%Y-%m-%dT%H:%M:%S:%f')
        return d

    @property
    def access_token_expired(self):
        return datetime.utcnow() > self.token_expiry

    @property
    def refresh_token_expired(self):
        return datetime.utcnow() > self.refresh_token_expiry

    @staticmethod
    def load(path):
        with open(path, 'r') as f:
            tokens = json.load(f)
            return oAuth_token(error=tokens.get('error'),
                               access_token=tokens.get('access_token'),
                               token_expiry=tokens.get('expires_in'),
                               refresh_token=tokens.get('refresh_token'),
                               refresh_token_expiry=tokens.get('refresh_token_expire_in'))

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.to_dict(True), f, indent=2)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)