import os
import pickle
from datetime import datetime
import pytz
from model.last_publication_retriever import LastPublicationRetriever


class LastPublicationFileRetriever(LastPublicationRetriever):
    def __init__(self, env_loader, my_logger):
        env_loader.load_dotenv()
        self.last_entry_file_path = os.getenv('LAST_ENTRY_FILE_PATH')
        self.my_logger = my_logger

    def get_file(self):
        return self.last_entry_file_path

    def save_file(self, last_entry_datetimes):
        with open(self.get_file(), 'wb') as last_entry_datetime_file:
            pickle.dump(last_entry_datetimes, last_entry_datetime_file)

    def last_time_saved(self):
        try:
            with open(self.get_file(), 'rb') as last_entry_datetime_file:
                self.my_logger.info("Loading last published date...")
                return pickle.load(last_entry_datetime_file)
        except Exception:
            self.my_logger.info("Load failed, taking current date")
            from datetime import timedelta
            last_entry_datetime = datetime.now(pytz.utc) - timedelta(10)
            return {'feed': last_entry_datetime, 'twitter': last_entry_datetime}

