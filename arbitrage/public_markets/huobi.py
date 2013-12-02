import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import time
from .market import Market


class Huobi(Market):
    def __init__(self):
        super(Huobi, self).__init__("CNY")
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        res = urllib.request.urlopen(
                'https://api.huobi.com/market/depth.php?a=marketdepth&random=0.%s' % int(time.time())
              )
        jsonstr = res.read().decode('utf8')
        try:
            data = json.loads(jsonstr)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
            return
        self.depth = self.format_depth(data["marketdepth"])

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[0]), 'amount': float(i[1])})
        return r

    def format_depth(self, depth):
        #bid buy order
        #ask sell order
        bids = self.sort_and_format(depth[0]['data'], True)
        asks = self.sort_and_format(depth[1]['data'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == "__main__":
    market = Huobi()
    print(market.get_depth())
