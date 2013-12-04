import logging
import config
from .observer import Observer


class StatsLogger(Observer):

    def __init__(self):
        self.total_profit = 0
        self.total_cny = 0
        self.total_btc = 0

        self.market_holds = {}

    def opportunity(self, profit, volume, buyprice, kask, sellprice, kbid, perc,
                    weighted_buyprice, weighted_sellprice):
        if perc < 1:
            return

        self.total_profit += profit
        self.total_cny += buyprice * volume
        self.total_btc += volume

        if kask not in self.market_holds:
            self.market_holds[kask] = {"CNY" : 0, "BTC" : 0, "PEAK_CNY" : 0, "PEAK_BTC" : 0}
        if kbid not in self.market_holds:
            self.market_holds[kbid] = {"CNY" : 0, "BTC" : 0, "PEAK_CNY" : 0, "PEAK_BTC" : 0}

        self.market_holds[kask]["CNY"] += buyprice * volume
        self.market_holds[kask]["PEAK_CNY"] = max(self.market_holds[kask]["CNY"], self.market_holds[kask]["PEAK_CNY"])
        self.market_holds[kask]["BTC"] -= volume

        self.market_holds[kbid]["BTC"] += volume
        self.market_holds[kbid]["PEAK_BTC"] = max(self.market_holds[kbid]["BTC"], self.market_holds[kbid]["PEAK_BTC"])
        self.market_holds[kbid]["CNY"] -= sellprice * volume

        logging.info("[stats] profit: %.4f", self.total_profit)

        for market, data in self.market_holds.items():
            logging.info("[stats] makret=%s , PEAK_CNY=%.4f, PEAK_BTC=%.4f", market, data['PEAK_CNY'], data['PEAK_BTC'])

