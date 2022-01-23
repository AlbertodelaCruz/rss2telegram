import os
import tweepy
import feedparser
from dotenv import load_dotenv
from pathlib import Path
import logging
import logging.handlers
from infrastructure.feed_parser_repository import FeedParserRepository


class EnvLoader:
    def load_dotenv(self):
        dotenv_path = Path('./system/.env')
        load_dotenv(dotenv_path=dotenv_path)


class Logger:
    @staticmethod
    def get_logger():
        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        my_logger.addHandler(handler)
        return my_logger


class TwitterAPI:
    def __init__(self, env_loader):
        env_loader.load_dotenv()
        twitter_api_key = os.getenv('TWITTER_API_KEY')
        twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
        auth.set_access_token(twitter_access_token, twitter_access_secret)
        self._api = tweepy.API(auth)

    def user_timeline(self, screen_name):
        return self._api.user_timeline(screen_name=screen_name)


def blog_parser_repository():
    return FeedParserRepository(feedparser)
