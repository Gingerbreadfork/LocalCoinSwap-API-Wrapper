from .config import api, log

def reset_allowance(ticker):
    ''' Reset Allowance (Typically Used with USDT)
        Returns: Status Code'''

    wallet_address = address(ticker)
    payload = {
        "currency": 19,
        "from_address": wallet_address
        }
    
    url = "wallets/allowance-reset/"
    response = api.post(url, data=payload)

    # Check if Sucessful & if not Log Warning
    if response.status_code == 400:
        result = response.json()
        log.warning(result['non_field_errors'][0]['message'])
    
    if response.status_code == 201:
        log.info(f"{ticker} Allowance for {wallet_address} Reset Sucessfully")

    return response.status_code


def create_tx(sender, receiver, amount):
    ''' Create Unsigned TX
        Returns: 500 Server Error - TODO: Fix This!'''
        
    payload = {
        "to_address": receiver,
        "from_address": sender,
        "amount": amount,
        }
    
    url = "wallets/unsigned/"
    response = api.post(url, data=payload)
    print(response.content)
    

def balance(ticker):
    ''' Get Wallet Balance (Non-Custodial)
            Returns: String'''

    # Collect Wallet Balance Based on Ticker
    url = f"wallets/info/{ticker.upper()}/"
    response = api.get(url)
    crypto_info = response.json()
    
    # If Bitcoin Select the Non-Custodial Wallet Specifically
    if ticker.upper() == "BTC":
        balance = str(crypto_info['nc_currency_balance']['total_balance'])
    else:
        balance = list(crypto_info['currency_balance'].values())[1]
    
    return balance


def address(ticker):
    ''' Get Wallet Address (Non-Custodial)
            Returns: String'''

    # Collect Wallet Address Based on Ticker
    url = f"wallets/info/{ticker.upper()}/"
    response = api.get(url)
    crypto_info = response.json()
    
    # If Bitcoin Select the Non-Custodial Wallet Specifically
    if ticker.upper() == "BTC":
        address = next(iter(crypto_info['nc_currency_balance']))
    else:
        address = crypto_info['wallets'][0]['address']

    return address


def custodial_withdrawal(crypto, destination, amount):
    ''' Custodial Withdrawal for Dash or Bitcoin
            Returns: Status Code '''
        
    if crypto.lower() == "btc" or crypto.lower() == "bitcoin":
        crypto_id = "1"
        log.info("Attempting Bitcoin Custodial Withdrawal")
    elif crypto.lower() == "dash":
        crypto_id = "15"
        log.info("Attempting Dash Custodial Withdrawal")
    else:
        log.warning("Crypto Type Invalid for Custodial Withdrawal")
        return 400
    
    payload = {
        "currency": crypto_id,
        "to_address": destination,
        "amount": amount
        }
    
    url = "wallets/custodial-withdrawal/"
    response = api.post(url, data=payload)
    
    if response.status_code == 400:
        log.warning("Witdraw Failed: Is it over the minimum amount?")
    elif response.status_code == 201:
        log.info("Withdrawal Initiated")
    else:
        log.warning("Unknown Error Occured")
        
    return response.status_code