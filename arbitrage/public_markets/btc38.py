import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import time
from .market import Market


class Btc38(Market):

    api_url = 'http://www.btc38.com/trade/getTradeList.php?coinname=BTC&n=0.%s' 

    def __init__(self):
        super(Btc38, self).__init__("CNY")
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        url = self.api_url % int(time.time())
        res = urllib.request.urlopen(url)
        jsonstr = res.read().decode('utf8')
        try:
            data = json.loads(jsonstr)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
        if data["result"] == "true":
            self.depth = self.format_depth(data)
        else:
            logging.error("%s - fetched data error" % (self.name))

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x['price']), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i['price']), 'amount': float(i['amount'])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['buyOrder'], True)
        asks = self.sort_and_format(depth['sellOrder'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == "__main__":
    market = Btc38()
    print(market.get_depth())
