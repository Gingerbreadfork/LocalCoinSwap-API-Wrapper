from .config import api, log

class Portfolio:
    def __init__(self):
        self.endpoint = "wallets/portfolio/"
        self.response = api.get(self.endpoint)
        self.data = self.response.json()
    
    @property
    def overview(self):
        ''' Get Portfolio Overview
                Returns: List of Dicts'''
        
        return self.data

    @property
    def value(self):
        ''' Get Total Portfolio Value in Fiat
                Returns: list [Value, Fiat Pair]'''

        value_list = [
            self.data["total_fiat_all_crypto"],
            self.data["local_currency_symbol"]
            ]

        return value_list
    
    def update(self):
        self.response = api.get(self.endpoint)
        self.data = self.response.json()
        log.info("Updated Portfolio Values")
        
    def clear(self):
        self.data = None
        log.info("Cleared Portfolio Values")

