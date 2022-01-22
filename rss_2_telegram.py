import time
import feedparser

from factory import EnvLoader, Logger, TwitterAPI
from infrastructure.twitter import Twitter
from infrastructure.blog import Blog
from model.last_entry_service import LastEntryService
from use_case.send_new_entries import SendNewEntries

if __name__ == "__main__":
    my_logger = Logger.get_logger()
    my_logger.info("Starting program")
    env_loader = EnvLoader()
    twitter_api = TwitterAPI(env_loader)
    twitter = Twitter(env_loader, twitter_api)
    feeder = Blog(env_loader, feedparser)
    last_entry_service = LastEntryService(env_loader, my_logger)

    last_entry_datetimes = last_entry_service.last_time_saved()

    send_entries_use_case = SendNewEntries(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes)

    while True:
        send_entries_use_case.send()
        time.sleep(60)
