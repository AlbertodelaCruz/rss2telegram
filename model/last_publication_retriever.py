class LastPublicationRetriever:
    def get_file(self):
        raise NotImplementedError

    def save_file(self, last_entry_datetimes):
        raise NotImplementedError

    def last_time_saved(self):
        raise NotImplementedError