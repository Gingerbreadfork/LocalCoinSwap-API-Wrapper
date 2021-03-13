from .config import api, log

class Fiat:
    def __init__(self):
        self.endpoint = "currencies/fiat-currencies/"
        self.params = {"limit": "200", "offset": "0"}
        self.response = api.get(self.endpoint, params=self.params)
        self.results = self.response.json()['results']

        if self.response.status_code == 200:
            log.info = "Payment Methods Gathered Sucessfully"
        else:
            log.warning = "Unable to Collect Payment Methods"

    @property
    def currencies(self):
        ''' Get List of Supported Fiat Base Pairs
            Returns: List of Dicts'''

        currency_list = []

        # Filter Primary Message Data from Response
        for currency in self.results:
            currency_data = dict(
                [
                    ('symbol', currency['symbol']),
                    ('title', currency['title']),
                    ]
                )

            currency_list.append(currency_data)

        return currency_list

    @property
    def tickers(self):
        ''' Get List of Supported Fiat Base Pairs - Tickers only
            Returns: List of Tickers/Symbols'''

        ticker_list = []

        # Filter Primary Message Data from Response
        for ticker in self.results:
            ticker_list.append(ticker['symbol'])

        return ticker_list

    @property
    def titles(self):
        ''' Get List of Supported Fiat Base Pairs - Titles only
            Returns: List of Tickers/Symbols'''

        title_list = []

        # Filter Primary Message Data from Response
        for title in self.results:
            title_list.append(title['title'])

        return title_list
    
    def update(self):
        ''' Refresh Currency Data
            Returns: Status Code of Request'''

        self.response = api.get(self.endpoint)
        self.results = self.response.json()['results']
        
        return self.response.status_code
