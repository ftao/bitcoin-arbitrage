import requests
import json
import logging
import config
import time
from .market import Market


class Z42Btc(Market):
    def __init__(self):
        super(Z42Btc, self).__init__("CNY")
        self.username = config.bitxf_username
        self.password = config.bitxf_password
        self.session = requests.Session()
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        depth = {}

        r = self.session.get('https://42btc.com/j/trade/depth/1-0?_=%s' %int(time.time()))
        jsonstr = r.text
        try:
            depth['asks'] = json.loads(jsonstr)[1]
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
            return 

        r = self.session.get('https://42btc.com/j/trade/depth/0-1?_=%s' %int(time.time()))
        jsonstr = r.text
        try:
            depth['bids'] = json.loads(jsonstr)[1]
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
            return 

        try:
            self.depth = self.format_depth(depth)
        except:
            logging.error("%s - fetched data error" % (self.name))
            logging.exception("error is: ")

    def sort_and_format_bids(self, l, reverse=False):
        l.sort(key=lambda x: float(x[6]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[6]), 'amount': float(i[5])})
        return r

    def sort_and_format_asks(self, l, reverse=False):
        l.sort(key=lambda x: float(x[6]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[6]), 'amount': float(i[3])})
        return r


    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bids'], True)
        asks = self.sort_and_format(depth['asks'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == "__main__":
    market = Z42Btc()
    print(market.get_depth())
