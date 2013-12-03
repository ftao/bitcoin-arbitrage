import requests
import json
import logging
import config
from .market import Market


class Bitxf(Market):
    def __init__(self):
        super(Bitxf, self).__init__("CNY")
        self.username = config.bitxf_username
        self.password = config.bitxf_password
        self.session = requests.Session()
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        r = self.session.get('https://bitxf.com/order_book.json', auth=(self.username, self.password))
        jsonstr = r.text
        try:
            data = r.json
            data = json.loads(jsonstr)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
        try:
            self.depth = self.format_depth(data)
        except:
            logging.error("%s - fetched data error" % (self.name))
            logging.exception("error is: ")

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x['ppc']), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i['ppc']), 'amount': float(i['amount'])})
        return r

    def format_depth(self, depth):
        #it's stupid, it's bid is sell order , it's ask is buy order
        bids = self.sort_and_format(depth['ask'], True)
        asks = self.sort_and_format(depth['bid'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == "__main__":
    market = Bitxf()
    print(market.get_depth())
