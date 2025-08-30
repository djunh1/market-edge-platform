
# import pytz
import requests

from datetime import datetime
from decimal import Decimal

from decouple import config
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlencode

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FMP_API_KEY = config("FMP_API_KEY", default=None, cast=str)


@dataclass
class FmpAPIClient:
    def __init__(self, ticker):
        self.ticker = ticker
    api_key: str = ""

    def get_api_key(self):
        return self.api_key or FMP_API_KEY
    
    def get_headers(self):
        api_key = self.get_api_key()
        return {}
    
    def get_params(self):
        return {
            "ticker": self.ticker,
            "apikey": self.get_api_key(),
        }
    
    def generate_url_historical_prices(self, pass_auth=False):
        path = f"/api/v3/historical-price-full/%s?timeseries=5000&apikey=%s" % (self.ticker, self.get_api_key())
        url = f'https://financialmodelingprep.com{path}'
        return url
    
    def fetch_data(self):
        headers = self.get_headers()
        url = self.generate_url_historical_prices()
        try:
            response = requests.get(url, headers=headers)
            #response.raise_for_status() # not 200/201
        except Exception as inst:
            logger.info("something went wrong.")

        return response.json()
    
    def get_stock_data(self):
        data = self.fetch_data()
        return data