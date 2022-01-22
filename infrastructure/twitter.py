from datetime import datetime
import requests
import os

import tweepy

from model.entry_service import EntryService


class Twitter(EntryService):
    def __init__(self, env_loader):
        env_loader.load_dotenv()
        twitter_api_key = os.getenv('TWITTER_API_KEY')
        twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        self.twitter_account = os.getenv('TWITTER_ACCOUNT')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot_chatID = os.getenv('BOT_CHATID')
        auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
        auth.set_access_token(twitter_access_token, twitter_access_secret)
        self.api = tweepy.API(auth)

    def get_new_entries(self, old_messages_datetime):
        timeline = self.api.user_timeline(screen_name=self.twitter_account)
        new_tweets = []
        for tweet in timeline:
            old_messages_datetime, new_tweets = self._append_new_tweets(tweet, new_tweets, old_messages_datetime)
        return old_messages_datetime, new_tweets

    def send_entries(self, entries):
        for entry in entries:
            telegram_body = {'chat_id':f'{self.bot_chatID}', 'parse_mode':'Markdown', 'text':f"{entry._json['text']}"}
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            _ = requests.post(url, json=telegram_body)

    def _append_new_tweets(self, tweet, tweets, old_messages_datetime):
        published_time = datetime.strptime(tweet._json['created_at'], "%a %b %d %H:%M:%S %z %Y")
        if published_time > old_messages_datetime:
            old_messages_datetime = published_time
            tweets.append(tweet)
        return old_messages_datetime, tweets