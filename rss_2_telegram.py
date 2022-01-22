import time
import feedparser

from factory import EnvLoader, Logger, TwitterAPI
from infrastructure.twitter import Twitter
from infrastructure.blog import Blog
from infrastructure.last_publication_file_retriever import LastPublicationFileRetriever
from use_case.send_new_publications import SendNewPublications

if __name__ == "__main__":
    my_logger = Logger.get_logger()
    my_logger.info("Starting program")
    env_loader = EnvLoader()
    twitter_api = TwitterAPI(env_loader)
    twitter = Twitter(env_loader, twitter_api)
    feeder = Blog(env_loader, feedparser)
    last_entry_service = LastPublicationFileRetriever(env_loader, my_logger)

    last_entry_datetimes = last_entry_service.last_time_saved()

    send_entries_use_case = SendNewPublications(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes)

    while True:
        send_entries_use_case.send()
        time.sleep(60)
