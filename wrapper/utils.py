from .config import api, log

def get_id(ticker):
    ''' Get ID for Specific Crypto
        Returns: int'''
        
    url = f"currencies/{ticker.upper()}/"
    response = api.get(url)
    crypto_info = response.json()
    crypto_id = int(crypto_info['id'])
    
    return crypto_id

