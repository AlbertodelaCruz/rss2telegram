class SendNewPublications:
    def __init__(self, my_logger, last_entry_service, twitter_publication_service, blog_publication_service, last_entry_datetimes):
        self._my_logger = my_logger
        self._last_entry_service = last_entry_service
        self._twitter_publication_service = twitter_publication_service
        self._blog_publication_service = blog_publication_service
        self._last_entry_datetimes = last_entry_datetimes

    def send(self):
        self._my_logger.info("Getting new entries...")
        self._last_entry_datetimes['feed'], new_feed_publications = self._blog_publication_service.get_new_publications(self._last_entry_datetimes['feed'])
        self._last_entry_datetimes['twitter'], new_twitter_publications = self._twitter_publication_service.get_new_publications(self._last_entry_datetimes['twitter'])

        for new_publication in new_feed_publications:
            self._my_logger.info(f"New feed entrie: {new_publication.title}")
        for new_publication in new_twitter_publications:
            self._my_logger.info(f"New twitter entrie: {new_publication.content}")

        self._last_entry_service.save_file(self._last_entry_datetimes)

        self._my_logger.info("Sending new entries...")
        self._blog_publication_service.send_publications(new_feed_publications)
        self._twitter_publication_service.send_publications(new_twitter_publications)
        self._my_logger.info("Entries sent...")