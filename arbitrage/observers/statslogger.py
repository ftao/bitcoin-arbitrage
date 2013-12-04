import logging
import config
from .observer import Observer


class StatsLogger(Observer):

    def __init__(self):
        self.total_profit = 0
        self.total_cny = 0
        self.total_btc = 0
        self.average_prec = 0

        self.market_holds = {}

    def opportunity(self, profit, volume, buyprice, kask, sellprice, kbid, perc,
                    weighted_buyprice, weighted_sellprice):
        perc_threshold = getattr(config, 'observer_logger_perc_threshold', 0)
        if perc < perc_threshold:
            return

        self.total_profit += profit

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


        for market, data in self.market_holds.items():
            logging.info("[stats] makret=%s , PEAK_CNY=%.4f, PEAK_BTC=%.4f", market, data['PEAK_CNY'], data['PEAK_BTC'])

        self.total_cny = sum([x['PEAK_CNY'] for x in self.market_holds.values()])
        self.total_btc = sum([x['PEAK_BTC'] for x in self.market_holds.values()])

        logging.info("[stats] profit: %.4f (%.4f%%) need CNY=%s BTC=%s",
                     self.total_profit, self.total_profit * 100.0 / self.total_cny / 2,
                     self.total_cny, self.total_btc)
