import time
import logging
import logging.handlers

from factory import EnvLoader, Logger
from twitter import Twitter
from feeder import Feeder
from last_entry_service import LastEntryService


def main(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes):
    my_logger.info("Getting new entries...")
    last_entry_datetimes['feed'], new_feed_entries = feeder.get_new_entries(last_entry_datetimes['feed'])
    last_entry_datetimes['twitter'], new_twitter_entries = twitter.get_new_entries(last_entry_datetimes['twitter'])
    for new_entrie in new_feed_entries:
        my_logger.info(f"New feed entrie: {new_entrie['title']}")
    for new_entrie in new_twitter_entries:
        my_logger.info(f"New twitter entrie: {new_entrie._json['text']}")
    last_entry_service.save_file(last_entry_datetimes)
    my_logger.info("Sending new entries...")
    feeder.send_entries(new_feed_entries)
    twitter.send_entries(new_twitter_entries)
    my_logger.info("Entries sent...")

if __name__ == "__main__":
    my_logger = Logger.get_logger()
    my_logger.info("Starting pogram")
    env_loader = EnvLoader()
    twitter = Twitter(env_loader)
    feeder = Feeder(env_loader)
    last_entry_service = LastEntryService(env_loader, my_logger)

    last_entry_datetimes = last_entry_service.last_time_saved()

    while True:
        main(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes)
        time.sleep(60)
