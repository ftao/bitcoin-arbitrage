from .btc38 import Btc38

class Btc38LTC(Btc38):

    api_url = 'http://www.btc38.com/trade/getTradeList.php?coinname=LTC&n=0.%s' 

if __name__ == "__main__":
    market = Btc38LTC()
    print(market.get_depth())
