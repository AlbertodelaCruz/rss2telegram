import feedparser
import time
from datetime import datetime, timedelta
import pytz
import requests
import pickle
import logging
import logging.handlers
import os
from dotenv import load_dotenv
from pathlib import Path
import tweepy
from tweepy import Cursor

dotenv_path = Path('./system/.env')
load_dotenv(dotenv_path=dotenv_path)


bot_token = os.getenv('BOT_TOKEN')
bot_chatID = os.getenv('BOT_CHATID')
blog_url = os.getenv('BLOG_URL')
feed_author = os.getenv('FEED_AUTHOR')
twitter_api_key = os.getenv('TWITTER_API_KEY')
twitter_api_secret = os.getenv('TWITTER_API_SECRET')
twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')
twitter_account = os.getenv('TWITTER_ACCOUNT')

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)


def get_new_entries(old_messages_datetime):
    feed = feedparser.parse(blog_url)
    entries = feed['entries']
    sorted_entries = sorted(entries, key=lambda d: d['published'])
    new_entries = []
    for entry in sorted_entries:
        published_time = datetime.strptime(entry['published'], "%a, %d %b %Y %H:%M:%S %z" )
        if published_time > old_messages_datetime and entry['author'] == feed_author:
            old_messages_datetime = published_time
            new_entries.append(entry)
    return old_messages_datetime, new_entries

def get_new_twitter_entries(old_messages_datetime):
    timeline = api.user_timeline(screen_name=twitter_account)
    new_tweets = []
    for tweet in timeline:
        published_time = datetime.strptime(tweet._json['created_at'], "%a %b %d %H:%M:%S %z %Y" )
        if published_time > old_messages_datetime:
            old_messages_datetime = published_time
            new_tweets.append(tweet)
    return old_messages_datetime, new_tweets

def send_feed_entries(entries):
    for entry in entries:
        my_logger.info(f"Publishing entry with: title {entry['title']}")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={entry['title']}"
        _ = requests.get(url)
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={entry['link']}"
        _ = requests.get(url)

def send_twitter_entries(entries):
    for entry in entries:
        my_logger.info(f"Publishing entry with: title {entry._json['text']}")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={entry._json['text']}"
        _ = requests.get(url)


my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)

try:
    with open('./last_entry_datetime', 'rb') as last_entry_datetime_file:
        my_logger.info("Loading last published date...")
        last_entry_datetimes = pickle.load(last_entry_datetime_file)
except Exception:
    my_logger.info("Load failed, taking current date")
    #from datetime import timedelta
    last_entry_datetime = datetime.now(pytz.utc)# - timedelta(3)
    last_entry_datetimes = {'feed': last_entry_datetime, 'twitter': last_entry_datetime}

my_logger.info("Starting program")
while True:
    my_logger.info("Getting new entries...")
    last_entry_datetimes['feed'], new_feed_entries = get_new_entries(last_entry_datetimes['feed'])
    last_entry_datetimes['twitter'], new_twitter_entries = get_new_twitter_entries(last_entry_datetimes['twitter'])
    for new_entrie in new_feed_entries:
        my_logger.info(f"New feed entrie: {new_entrie['title']}")
    for new_entrie in new_twitter_entries:
        my_logger.info(f"New twitter entrie: {new_entrie._json['text']}")
    with open('./last_entry_datetime', 'wb') as last_entry_datetime_file:
        pickle.dump(last_entry_datetimes, last_entry_datetime_file)
    my_logger.info("Sending new entries...")
    send_feed_entries(new_feed_entries)
    send_twitter_entries(new_twitter_entries)
    my_logger.info("Entries sent...")
    time.sleep(60)
