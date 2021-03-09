from .config import api, log

def get(limit=10):
    ''' Get Notifications
        Returns: List of Dicts'''

    url = "notifications/"
    params = {"limit": limit}
    response = api.get(url, params=params)
    notifications = response.json()['results']
        
    return notifications

