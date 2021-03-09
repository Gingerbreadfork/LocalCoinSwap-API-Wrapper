import logging
from dotenv import load_dotenv
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Start Logger
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO)
log = logging.getLogger(__name__)

# Load API Key from .env
load_dotenv()
token = os.getenv("TOKEN")


class RequestsApi:
    def __init__(self, base_url, **kwargs):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Token {token}'})

        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
            )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def request(self, method, url, **kwargs):
        return self.session.request(method, self.base_url+url, **kwargs)

    def head(self, url, **kwargs):
        return self.session.head(self.base_url+url, **kwargs)

    def get(self, url, **kwargs):
        return self.session.get(self.base_url+url, **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(self.base_url+url, **kwargs)

    def put(self, url, **kwargs):
        return self.session.put(self.base_url+url, **kwargs)

    def patch(self, url, **kwargs):
        return self.session.patch(self.base_url+url, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(self.base_url+url, **kwargs)

    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestsApi.__deep_merge(value, node)
            else:
                destination[key] = value
        return destination

api = RequestsApi("https://localcoinswap.com/api/v2/")


