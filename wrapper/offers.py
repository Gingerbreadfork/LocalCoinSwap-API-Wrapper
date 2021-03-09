from .config import api, log

def get(limit=100):
    ''' Get Your Trade Offers
        Returns: List of Dicts'''
        
    response = api.get("offers/")
    offer_data = response.json()['results']
    
    offers = []

    # Filter Primary Offer Data from Response
    for offer in offer_data:
        offer_dict = dict(
            [
                ('crypto', offer['coin_currency']['symbol']),
                ('fiat', offer['fiat_currency']['symbol']),
                ('headline', offer['headline']),
                ('hidden', offer['hidden']),
                ('min_size', offer['min_trade_size']),
                ('max_size', offer['max_trade_size']),
                ('enforced_sizes', offer['enforced_sizes']),
                ('location', offer['location_name']),
                ('country', offer['country_code']),
                ('payment_method', offer['payment_method']['name']),
                ('type', offer['trading_type']['name'])
                ]
            )

        offers.append(offer_dict)

    return offers


def search(
    limit=10,
    ticker=None,
    trade_type=None,
    username=None,
    payment=None,
    country=None
    ):
    
    ''' Search All Trade Offers
        Returns: List of Dicts'''
        
    params = {
        'limit': limit,
        'coin_currency': ticker,
        'trading_type': trade_type,
        }
    
    if username is not None:
        params['username'] = username
    
    if trade_type is not None:
        params['trading_type'] = trade_type
        
    if ticker is not None:
        params['coin_currency'] = ticker
        
    if payment is not None:
        params['payment_method'] = payment
        
    if username is not None:
        params['username'] = username
    
    if country is not None:
        params['country_code'] = country
    
    url = "offers/search/"
    response = api.get(url, params=params)
    offer_data = response.json()['results']
    
    offers = []

    # Filter Primary Offer Data from Response
    for offer in offer_data:
        offer_dict = dict(
            [
                ('creator', offer['created_by']['username']),
                ('crypto', offer['coin_currency']['symbol']),
                ('fiat', offer['fiat_currency']['symbol']),
                ('headline', offer['headline']),
                ('min_size', offer['min_trade_size']),
                ('max_size', offer['max_trade_size']),
                ('enforced_sizes', offer['enforced_sizes']),
                ('location', offer['location_name']),
                ('country', offer['country_code']),
                ('payment_method', offer['payment_method']['name']),
                ('type', offer['trading_type']['name'])
                ]
            )

        offers.append(offer_dict)

    return offers

def delete(uuid):
    ''' Delete Trade Offer from UUID
        Returns: Status Code 204 Sucess or 404 Not Found'''
    
    url = f"offers/{uuid}"
    response = api.delete(url)

    if response.status_code == 204:
            log.info(f'Trade: {uuid} Deleted Sucessfully')
            
    if response.status_code == 404:
            log.warning(f'Trade: {uuid} Not Found or Already Deleted')
    
    return response.status_code
    