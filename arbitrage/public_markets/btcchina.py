import urllib.request
import urllib.error
import urllib.parse
import hmac
import hashlib
import re
import time
import json
import base64
import logging
import config
from .market import Market


class BtcChina(Market):
    def __init__(self):
        super(BtcChina, self).__init__("CNY")
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

        self.access_key=config.btcchina_key
        self.secret_key=config.btcchina_secret
        self.api_root = 'https://api.btcchina.com/api_trade_v1.php'

    def update_depth(self):
        post_data = {}
        post_data['method']='getMarketDepth2'
        post_data['params']=[100]
        data =  self._private_request(post_data)
        if data is not None:
            self.depth = self.format_depth(data['market_depth'])

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x["price"]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i["price"]), 'amount': float(i["amount"])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bid'], True)
        asks = self.sort_and_format(depth['ask'], False)
        return {'asks': asks, 'bids': bids}

    def _get_tonce(self):
        return int(time.time()*1000000)
 
    def _get_params_hash(self,pdict):
        pstring=""
        # The order of params is critical for calculating a correct hash
        fields=['tonce','accesskey','requestmethod','id','method','params']
        for f in fields:
            if pdict[f]:
                if f == 'params':
                    # Convert list to string, then strip brackets and spaces
                    # probably a cleaner way to do this
                    param_string=re.sub("[\[\] ]","",str(pdict[f]))
                    param_string=re.sub("'",'',param_string)
                    pstring+=f+'='+param_string+'&'
                else:
                    pstring+=f+'='+str(pdict[f])+'&'
            else:
                pstring+=f+'=&'
        pstring=pstring.strip('&')
 
        # now with correctly ordered param string, calculate hash
        phash = hmac.new(bytes(self.secret_key, "UTF-8"), bytes(pstring, "UTF-8"), hashlib.sha1).hexdigest()
        return phash

    def _private_request(self, post_data):
        #fill in common post_data parameters
        tonce=self._get_tonce()
        post_data['tonce'] = tonce
        post_data['accesskey'] = self.access_key
        post_data['requestmethod'] = 'post'
 
        # If ID is not passed as a key of post_data, just use tonce
        if not 'id' in post_data:
            post_data['id'] = tonce
 
        pd_hash=self._get_params_hash(post_data)
 
        # must use b64 encode        
        auth_string = 'Basic ' + str(base64.b64encode(bytes(self.access_key+':'+pd_hash, "UTF-8")), "UTF-8")
        headers = {'Authorization' : auth_string, 'Json-Rpc-Tonce' : tonce}
 
        try:
            req = urllib.request.Request(self.api_root,
                                         bytes(json.dumps(post_data), "UTF-8"),
                                         headers)
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                jsonstr = response.read()
                resp_dict = json.loads(str(jsonstr, "UTF-8"))
                if str(resp_dict['id']) == str(post_data['id']):
                    if 'result' in resp_dict:
                        return resp_dict['result']
                    elif 'error' in resp_dict:
                        logging.error('Got error when request BTCChina, %s' % resp_dict['error'])
                else:
                    logging.error('Got error when request BTCChina, %s' % "id not match")
        except Exception as err:
            logging.error('Can\'t request BTCChina, %s' % err)

        return None

if __name__ == "__main__":
    market = BtcChina()
    print(market.get_depth())
