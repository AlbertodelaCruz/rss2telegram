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

dotenv_path = Path('./system/.env')
load_dotenv(dotenv_path=dotenv_path)


bot_token = os.getenv('BOT_TOKEN')
bot_chatID = os.getenv('BOT_CHATID')
blog_url = os.getenv('BLOG_URL')
feed_author = os.getenv('FEED_AUTHOR')


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

def send_entries(entries):
    for entry in entries:
        my_logger.info(f"Publishing entry with: title {entry['title']}")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={entry['title']}"
        _ = requests.get(url)
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={entry['link']}"
        _ = requests.get(url)


my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)

try:
    with open('./last_entry_datetime', 'rb') as last_entry_datetime_file:
        my_logger.info("Loading last published date...")
        last_entry_datetime = pickle.load(last_entry_datetime_file)
except Exception:
    my_logger.info("Load failed, taking current date")
    #from datetime import timedelta
    last_entry_datetime = datetime.now(pytz.utc)# - timedelta(3)

my_logger.info("Starting program")
while True:
    my_logger.info("Getting new entries...")
    last_entry_datetime, new_entries = get_new_entries(last_entry_datetime)
    for new_entrie in new_entries:
        my_logger.info(f"New entrie: {new_entrie['title']}")
    with open('./last_entry_datetime', 'wb') as last_entry_datetime_file:
        pickle.dump(last_entry_datetime, last_entry_datetime_file)
    my_logger.info("Sending new entries...")
    send_entries(new_entries)
    my_logger.info("Entries sent...")
    time.sleep(60)
