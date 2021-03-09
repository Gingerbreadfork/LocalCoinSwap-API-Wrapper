from .config import api, log


def currencies(limit=200, offset=0):
    ''' Get List of Supported Fiat Base Pairs
        Returns: List of Dicts'''

    params = {'limit': limit, 'offset': offset}
    url = "currencies/fiat-currencies/"
    response = api.get(url, params=params)
    methods_response = response.json()['results']

    methods = []

    # Filter Primary Message Data from Response
    for method in methods_response:
        message_data = dict(
            [
                ('symbol', method['symbol']),
                ('title', method['title']),
                ]
            )

        methods.append(message_data)

    return methods


def tickers(limit=200, offset=0):
    ''' Get List of Supported Fiat Base Pairs - Tickers only
        Returns: List of Tickers/Symbols'''

    params = {'limit': limit, 'offset': offset}
    url = "currencies/fiat-currencies/"
    response = api.get(url, params=params)
    methods_response = response.json()['results']

    methods = []

    # Filter Primary Message Data from Response
    for method in methods_response:
        methods.append(method['symbol'])

    return methods


def titles(limit=200, offset=0):
    ''' Get List of Supported Fiat Base Pairs - Titles only
        Returns: List of Tickers/Symbols'''

    params = {'limit': limit, 'offset': offset}
    url = "currencies/fiat-currencies/"
    response = api.get(url, params=params)
    methods_response = response.json()['results']

    if response.status_code == 200:
        log.info = "Payment Methods Gathered Sucessfully"
    else:
        log.warning = "Unable to Collect Payment Methods"

    methods = []

    # Filter Primary Message Data from Response
    for method in methods_response:
        methods.append(method['title'])

    return methods
