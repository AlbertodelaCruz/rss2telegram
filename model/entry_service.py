class EntryService:
    def get_new_publications(self, old_messages_datetime):
        raise NotImplementedError

    def send_publications(self, entries):
        raise NotImplementedError