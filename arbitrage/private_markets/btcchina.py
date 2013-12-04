from public_markets.btcchina import BtcChinaMixin
from .market import Market


class PrivateBtcChina(Market, BtcChinaMixin):

    def __init__(self):
        Market.__init__(self)
        BtcChinaMixin.__init__(self)
        self.cny_balance = 0
        self.get_info()

    def __str__(self):
        return "%s: %s" % (self.name, str({"btc_balance": self.btc_balance,
                                           "cny_balance": self.cny_balance}))

    def get_info(self):
        info = self.get_account_info()
        self.cny_balance = float(info['balance']['cny']['amount'])
        self.btc_balance = float(info['balance']['btc']['amount'])

    def buy(self, amount, price):
        post_data = {}
        post_data['method'] = 'buyOrder'
        post_data['params'] = [price,amount]
        return self._private_request(post_data)


    def sell(self, amount, price):
        post_data = {}
        post_data['method'] = 'sellOrder'
        post_data['params'] = [price,amount]
        return self._private_request(post_data)
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)

    def get_account_info(self):
        post_data = {}
        post_data['method']='getAccountInfo'
        post_data['params']=[]
        return self._private_request(post_data)

if __name__ == "__main__":
    market = PrivateBtcChina()
    print(market.get_depth())
