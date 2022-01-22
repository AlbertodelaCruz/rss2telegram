class EntryService:
    def get_new_entries(self, old_messages_datetime):
        raise NotImplementedError

    def send_entries(self, entries):
        raise NotImplementedError