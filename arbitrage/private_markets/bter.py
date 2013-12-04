import requests
import time
import urllib
import hmac
import hashlib
import logging

import config
from private_markets.market import Market

class PrivateBter(Market):

    api_root = 'https://bter.com/api/1/'

    def __init__(self):
        Market.__init__(self)
        self.access_key = config.bter_key
        self.secret_key = config.bter_secret
        self.pair = getattr(config, 'bter_pair', 'btc_cny')
        self.cny_balance = 0
        self.account_info = {}

        self.session = requests.session()
        self.get_info()

    def __str__(self):
        return str(self.account_info)

    def get_info(self):
        self.account_info = self.get_account_info()

    def buy(self, amount, price):
        post_data = {}
        post_data['pair'] = self.pair
        post_data['type'] = 'BUY'
        post_data['rate'] = price
        post_data['amount'] = amount
        resp =  self._private_request('private/placeorder', post_data)
        if resp["result"] == "true":
            return True
        else:
            logging.warn("fail to buy , req is %s, resp is %s", post_data, resp)
            return False

    def sell(self, amount, price):
        post_data = {}
        post_data['pair'] = self.pair
        post_data['type'] = 'SELL'
        post_data['rate'] = price
        post_data['amount'] = amount
        resp =  self._private_request('private/placeorder', post_data)
        if resp["result"] == "true":
            return True
        else:
            logging.warn("fail to sell , req is %s, resp is %s", post_data, resp)
            return False

    def get_account_info(self):
        post_data = {}
        resp =  self._private_request('private/getfunds', post_data)
        if resp["result"] != "true":
            logging.warn("fail to getfunds , req is %s, resp is %s", post_data, resp)
        return resp

    def _get_nonce(self):
        return int(time.time()*1000000)
 
    def _private_request(self, path, params):
        nonce = self._get_nonce()
        params['nonce'] = nonce
        urlparams = bytes(urllib.parse.urlencode(params), "UTF-8")
        secret = bytes(self.secret_key, "UTF-8")
        sign = hmac.new(secret, urlparams, hashlib.sha512).hexdigest()

        headers = {"Key" : self.access_key, "Sign" : str(sign)}

        resp = self.session.post(self.api_root + path, data=urlparams, headers=headers)
        try:
            return resp.json()
        except Exception as err:
            logging.error('Can\'t request Bter, %s' % err)
            logging.exception("detail is :")

if __name__ == "__main__":
    market = PrivateBter()
    #market.buy(1, 0.1)
    #market.sell(1, 1000)
    #market.get_info()
    print(market)
