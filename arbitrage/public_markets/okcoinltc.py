import urllib.request
import urllib.error
import urllib.parse
import json
import logging

from .okcoin import OkCoin
#NOT REALTIME
class OkCoinLTC(OkCoin):
    api_url = 'https://www.okcoin.com/api/depth.do?symbol=ltc_cny'

if __name__ == "__main__":
    market = OkCoinLTC()
    print(market.get_depth())
