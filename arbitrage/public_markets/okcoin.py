import urllib.request
import urllib.error
import urllib.parse
import json
import logging
from .market import Market


#NOT REALTIME
class OkCoin(Market):

    api_url = 'https://www.okcoin.com/api/depth.do'

    def __init__(self):
        super(OkCoin, self).__init__("CNY")
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        res = urllib.request.urlopen(self.api_url)
        jsonstr = res.read().decode('utf8')
        try:
            data = json.loads(jsonstr)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
            return
        self.depth = self.format_depth(data)

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[0]), 'amount': float(i[1])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bids'], True)
        asks = self.sort_and_format(depth['asks'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == "__main__":
    market = OkCoin()
    print(market.get_depth())
