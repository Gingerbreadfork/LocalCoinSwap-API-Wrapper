from .config import api, log
from datetime import datetime


def trades(alive=True, limit=10):
    ''' List Trades of All Stutuses
            Returns: List of Dicts'''
    
    # Is the request for past or active trades?
    if alive is True:
        stage = "live"
    else:
        stage = "past"
    
    # Get Trade List from API
    params = {'limit': limit, 'stage': stage}
    url = "trades/list"
    response = api.get(url, params=params)
    trade_list = response.json()

    # Filter Primary Trade Info from Response
    trades = []
    for trade in trade_list['results']:
        individual_trade = dict(
            [
                ('uuid', trade['uuid']),
                ('crypto', trade['coin_currency']['symbol']),
                ('buyer', trade['buyer']['username']),
                ('seller', trade['seller']['username']),
                ('status', trade['status'])
                ]
            )

        # Add to List of Trades
        trades.append(individual_trade)
        
    log.info(f"Trades Retrieved: {len(trades)}")
        
    return trades


def messages(uuid, limit=100):
    ''' Get Trade Messages from a Specific Trade
            Returns: List of Dicts'''

    params = {'limit': limit}
    url = f"trades/message/list/{uuid}"
    response = api.get(url, params=params)
    trade_message_data = response.json()['results']

    messages = []

    # Filter Primary Message Data from Response
    for message in trade_message_data:
        time_object = datetime.fromtimestamp(message['time_created'])
        timestamp = time_object.strftime("%Y-%m-%d %H:%M:%S")
        message_data = dict(
            [
                ('username', message['created_by']['username']),
                ('content', message['content']),
                ('timestamp', timestamp),
                ]
            )

        messages.append(message_data)

    return messages


def send_message(uuid, content):
    ''' Send Message to a Specific Trade
            Returns: Status Code'''
            
    payload = {'content': content}
    url = f"trades/message/{uuid}/"
    response = api.post(url, data=payload)
    result = response.status_code

    # Check if Message Sent Sucessfully
    if result == 201:
        log.info(f"Sent Message: {content} - Trade: {uuid}")
    else:
        log.warning(f"Sending Message Failed - Trade: {uuid}")

    return result


def status(uuid):
    ''' Quickly Check Status of Trade by Providing UUID
        Returns: Trade Status as String'''
    
    url = f"trades/{uuid}/status/"
    response = api.get(url)
    status = response.json()['status']

    return status


def leave_feedback(rating, feedback, trade,):
    ''' Leave Feedback on a Trade
        Returns: Status Code'''

    payload = {
        "rating": rating,
        "feedback": feedback,
        "trade": trade
        }

    url = "trades/feedback/create/"
    response = api.post(url, data=payload)
    result = response.status_code
    
    if result == 201:
        log.info(f"Feedback: {feedback} - Rating: {rating} - Left on Trade: {trade}")
    
    if result == 400:
        log.warning(f"Unable to Leave Feedback on Trade: {trade}")
        
    return result


def create_custodial(uuid, amount, value):
    ''' Request to Start a Custodial Trade
        Returns: Status Code'''

    payload = {
        "fiat_amount": value,
        "coin_amount": amount,
        "offer": uuid
        }

    url = "trades/custodial/create/"
    response = api.post(url, data=payload)
    
    if response.status_code == 400:
        log.warning(response.json()['non_field_errors'][0]['message'])
        
    if response.status_code == 201:
        log.info(f"Trade: {uuid} - Status: {response.json()['status']}")

    return response.status_code


def change_status_custodial(uuid, status):
    ''' Change Status of a Custodial Trade (BTC-NC/DASH)
        Returns: Status Code'''

    payload = {"status": status}
    url = f"trades/custodial/update/{uuid}/"    
    response = api.patch(url, data=payload)
    
    if response.status_code == 400:
        try:
            log.warning(response.json()['status'][0]['message'])
        except:
            log.warning(response.json()['non_field_errors'][0]['message'])
        
    if response.status_code == 200:
        log.info(f"Trade: {uuid} - Status Changed: {response.json()['status']}")

    return response.status_code


def change_status(uuid, status):
    ''' Change Status of Non-Custodial Trade
        Returns: Status Code'''

    payload = {"status": status}
    url = f"trades/non-custodial/update/{uuid}/"
    response = api.patch(url, data=payload)
    
    if response.status_code == 400:
        try:
            log.warning(response.json()['status'][0]['message'])
        except:
            log.warning(response.json()['non_field_errors'][0]['message'])
        
    if response.status_code == 200:
        log.info(f"Trade: {uuid} - Status Changed: {response.json()['status']}")

    return response.status_code


def invoice(uuid):
    ''' Get Invoice for Specific Trade
        Returns: Link to PDF File as String'''
    
    url = f"trades/{uuid}/invoice/"
    response = api.post(url)
    pdf_link = response.json()['response']
    
    return pdf_link

def latest(*args):
    ''' Get UUID of Most Recent Trade
        Returns UUID as String'''
        
    stage = "live"
    
    # Is the request for past or active trades?
    if "past" in args:
        stage = "past"
        
    # Get Most Recent Trade from API
    params = {'limit': 1, 'stage': stage}
    url = "trades/list"
    response = api.get(url, params=params)
    most_recent_uuid = response.json()['results'][0]['uuid']
    log.info(f"Latest Trade UUID:{most_recent_uuid}")
    
    return most_recent_uuid
        
        
        
        
        
        
        
        
        
