import urllib.request
import urllib.error
import urllib.parse
import json
import logging
from .market import Market

from .bter import Bter

class BterLTC(Bter):

    api_url = 'https://bter.com/api/1/depth/ltc_cny'

if __name__ == "__main__":
    market = BterLTC()
    print(market.get_depth())
