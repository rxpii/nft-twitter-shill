import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        # api keys
        self.API_KEY = os.getenv('API_KEY')
        self.API_KEY_SECRET = os.getenv('API_KEY_SECRET')
        self.BEARER_TOKEN = os.getenv('BEARER_TOKEN')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

        # settings
        self.CHECK_DELAY = int(os.getenv('CHECK_DELAY'))
        self.REPLY_DELAY = int(os.getenv('REPLY_DELAY'))
        self.REPLY_VARIANCE_DELAY = int(os.getenv('REPLY_VARIANCE_DELAY'))
        self.RATE_LIMIT_DELAY = int(os.getenv('RATE_LIMIT_DELAY'))
        self.MIN_RETWEETS = int(os.getenv('MIN_RETWEETS'))
        self.FETCH_COUNT = int(os.getenv('FETCH_COUNT'))

        # content
        self.SHILL_MSG = os.getenv('SHILL_MSG')

    def update_msg(self):
        load_dotenv()
        self.SHILL_MSG = os.getenv('SHILL_MSG')
