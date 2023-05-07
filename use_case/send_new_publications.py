class SendNewPublications:
    def __init__(self, my_logger, last_entry_service, twitter_publication_service, blog_publication_service, last_entry_datetimes, telegram_notifier_service, blog_board_message_publication_service, last_board_message_service, birthday_service):
        self._my_logger = my_logger
        self._last_entry_service = last_entry_service
        self._twitter_publication_service = twitter_publication_service
        self._blog_publication_service = blog_publication_service
        self._last_entry_datetimes = last_entry_datetimes
        self._telegram_notifier_service = telegram_notifier_service
        self._blog_board_message_publication_service = blog_board_message_publication_service
        self._last_board_message_service = last_board_message_service
        self._birthday_service = birthday_service

    def send(self):
        last_board_message, publications = self._retrieve_publications_from_source()
        self._last_entry_service.save_file(self._last_entry_datetimes)
        self._last_board_message_service.save(last_board_message)
        self._send_publications(publications)

    def _send_publications(self, publications):
        self._my_logger.info("Sending new publications...")
        self._telegram_notifier_service.send_publications(publications)
        self._my_logger.info("Publications sent...")

    def _retrieve_publications_from_source(self):
        self._my_logger.info("Getting new publications...")
        self._last_entry_datetimes['feed'], new_feed_publications = self._blog_publication_service.get_new_publications(self._last_entry_datetimes['feed'])
        self._last_entry_datetimes['twitter'], new_twitter_publications = self._twitter_publication_service.get_new_publications(self._last_entry_datetimes['twitter'])
        last_board_message, new_board_message_publications = self._blog_board_message_publication_service.get_new_publications(self._last_board_message_service.get_message())
        birthday_publications = self._birthday_service.get_new_publications()
        publications = new_feed_publications + new_twitter_publications + new_board_message_publications + birthday_publications
        for publication in publications:
            self._my_logger.info(f"New publication: {publication.title or publication.content}")
        return last_board_message, publications
