import time
from datetime import datetime, timedelta
import pytz
import pickle
import logging
import logging.handlers
import os

from factory import EnvLoader
from twitter import Twitter
from feeder import Feeder


my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

env_loader = EnvLoader()
twitter = Twitter(env_loader)
feeder = Feeder(env_loader)

def main(env_loader, my_logger, twitter, feeder):
    my_logger.info("Getting new entries...")
    last_entry_datetimes['feed'], new_feed_entries = feeder.get_new_entries(last_entry_datetimes['feed'])
    last_entry_datetimes['twitter'], new_twitter_entries = twitter.get_new_entries(last_entry_datetimes['twitter'])
    for new_entrie in new_feed_entries:
        my_logger.info(f"New feed entrie: {new_entrie['title']}")
    for new_entrie in new_twitter_entries:
        my_logger.info(f"New twitter entrie: {new_entrie._json['text']}")
    with open('./last_entry_datetime', 'wb') as last_entry_datetime_file:
        pickle.dump(last_entry_datetimes, last_entry_datetime_file)
    my_logger.info("Sending new entries...")
    feeder.send_entries(new_feed_entries)
    twitter.send_entries(new_twitter_entries)
    my_logger.info("Entries sent...")

try:
    with open('./last_entry_datetime', 'rb') as last_entry_datetime_file:
        my_logger.info("Loading last published date...")
        last_entry_datetimes = pickle.load(last_entry_datetime_file)
except Exception:
    my_logger.info("Load failed, taking current date")
    #from datetime import timedelta
    last_entry_datetime = datetime.now(pytz.utc) - timedelta(10)
    last_entry_datetimes = {'feed': last_entry_datetime, 'twitter': last_entry_datetime}

if __name__ == "__main__":
    my_logger.info("Starting pogram")
    while True:
        main(env_loader, my_logger, twitter, feeder)
        time.sleep(60)
