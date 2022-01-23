import time

from factory import EnvLoader, Logger, TwitterAPI, blog_parser_repository
from model.twitter_publication_service import TwitterPublicationService
from model.blog_publication_service import BlogPublicationService
from infrastructure.last_publication_file_retriever import LastPublicationFileRetriever
from use_case.send_new_publications import SendNewPublications

if __name__ == "__main__":
    my_logger = Logger.get_logger()
    my_logger.info("Starting program")
    env_loader = EnvLoader()
    twitter_api = TwitterAPI(env_loader)
    twitter_publication_service = TwitterPublicationService(env_loader, twitter_api)
    blog_publication_service = BlogPublicationService(env_loader, blog_parser_repository())
    last_entry_service = LastPublicationFileRetriever(env_loader, my_logger)

    last_entry_datetimes = last_entry_service.last_time_saved()

    send_entries_use_case = SendNewPublications(my_logger, last_entry_service, twitter_publication_service, blog_publication_service, last_entry_datetimes)

    while True:
        send_entries_use_case.send()
        time.sleep(60)
