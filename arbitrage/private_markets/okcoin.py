import requests
import random
import json
import logging
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose



import config
from private_markets.market import Market

class PrivateOkCoin(Market):

    url_root = 'https://www.okcoin.com'

    default_headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip,deflate,sdch",
        "Accept-Language":"en,zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4",
        "Origin" : "http://www.okcoin.com",
        "Referer" : "http://www.okcoin.com/buy.do",
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self):
        Market.__init__(self)

        #self.cookie = config.okcoin_cookie 
        self.username = config.okcoin_username
        self.password = config.okcoin_password
        self.trade_password = config.okcoin_trade_password

        self.is_login = False

        #self.pair = getattr(config, 'bter_pair', 'btc_cny')
        self.balance = {}

        self.session = requests.session()
        headers = {} #'Cookie' : self.cookie}
        headers.update(self.default_headers)
        self.session.headers = headers

        self._login()
        self.get_info()

    def __str__(self):
        return str(self.balance)

    def _login(self):
        resp = self.session.get(self.url_root)

        login_url = self.url_root + '/login/index.do?random=%s' % random.randint(1, 100)

        post_data = {
            "loginName": self.username, 
            "password": self.password, 
        }

        resp = self.session.post(login_url, post_data)
        data = json.loads(resp.text)
        self.is_login = (data['errorNum'] == 0 and data['resultCode'] == 0)

    def get_info(self):
        resp = self.session.get(self.url_root)
        soup = BeautifulSoup(resp.text)
        amounts = [float(x.string) for x in soup.find_all('span', class_="num1-title3")[:3]]
        self.balance = {"CNY" : amounts[0], "BTC" : amounts[1], "LTC" : amounts[2]}

    def get_balance(self, currency):
        try:
            return float(self.balance.get(currency.upper(), 0))
        except:
            return 0

    def buy_ltc(self, amount, price):
        return self._buy(1, amount, price)

    def sell_ltc(self, amount, price):
        return self._sell(1, amount, price)

    buy = buy_ltc
    sell = sell_ltc

    def _buy(self, symbol, amount, price):
        url = self.url_root + '/trade/buyBtcSubmit.do?random=%s' % random.randint(1, 100)
        post_data = {
            "tradeAmount": amount,
            "tradeCnyPrice": price,
            "tradePwd": self.trade_password,
            "symbol": symbol
        }
        #print(buy_url, post_data)
        resp = self.session.post(url, post_data)
        data = json.loads(resp.text)

        logging.info('buy result:%s', data)

        if data['errorNum'] == 0 and data['resultCode'] == 0:
            logging.info('buy success')
        else:
            logging.info('buy fail')

    def _sell(self, symbol, amount, price):
        url = self.url_root + '/trade/sellBtcSubmit.do?random=%s' % random.randint(1, 100)
        post_data = {
            "tradeAmount": amount,
            "tradeCnyPrice": price,
            "tradePwd": self.trade_password,
            "symbol": symbol
        }
        resp = self.session.post(url, post_data)
        data = json.loads(resp.text)

        logging.info('sell result: %s', data)

        if data['errorNum'] == 0 and data['resultCode'] == 0:
            logging.info('sell success')
        else:
            logging.info('sell fail')

    def get_account_info(self):
        pass


if __name__ == "__main__":
    market = PrivateOkCoin()
    #market.buy_ltc(0.1, 103)
    #market.sell_ltc(0.1, 1000)
    #market.buy(1, 0.1)
    #market.sell(1, 1000)
    #market.get_info()
    print(market)
    print("CNY", market.get_balance('CNY'))
    print("LTC", market.get_balance('LTC'))
