import logging
import config
from .observer import Observer


class Logger(Observer):

    def opportunity(self, profit, volume, buyprice, kask, sellprice, kbid, perc,
                    weighted_buyprice, weighted_sellprice):
        perc_threshold = getattr(config, 'observer_logger_perc_threshold', 0)
        if perc < perc_threshold:
            return 
        currency = getattr(config, 'main_currency', 'USD')
        logging.info("profit: %f %s with volume: %f BTC - buy at %.4f (%s) sell at %.4f (%s) ~%.2f%%" % (
            profit, currency, volume, buyprice, kask, sellprice, kbid, perc))
