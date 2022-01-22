class SendNewPublications:
    def __init__(self, my_logger, last_entry_service, twitter, feeder, last_entry_datetimes):
        self._my_logger = my_logger
        self._last_entry_service = last_entry_service
        self._twitter = twitter
        self._feeder = feeder
        self._last_entry_datetimes = last_entry_datetimes

    def send(self):
        self._my_logger.info("Getting new entries...")
        self._last_entry_datetimes['feed'], new_feed_publications = self._feeder.get_new_publications(self._last_entry_datetimes['feed'])
        self._last_entry_datetimes['twitter'], new_twitter_publications = self._twitter.get_new_publications(self._last_entry_datetimes['twitter'])

        for new_publication in new_feed_publications:
            self._my_logger.info(f"New feed entrie: {new_publication.title}")
        for new_publication in new_twitter_publications:
            self._my_logger.info(f"New twitter entrie: {new_publication.content}")

        self._last_entry_service.save_file(self._last_entry_datetimes)

        self._my_logger.info("Sending new entries...")
        self._feeder.send_publications(new_feed_publications)
        self._twitter.send_publications(new_twitter_publications)
        self._my_logger.info("Entries sent...")