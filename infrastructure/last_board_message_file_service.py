import os
import pickle
from datetime import datetime

from model.last_board_message_service import LastBoardMessageService


class LastBoardMessageFileService(LastBoardMessageService):
    def __init__(self, env_loader, my_logger):
        env_loader.load_dotenv()
        self.last_entry_file_path = os.getenv('LAST_ENTRY_BOARD_MESSAGE_FILE_PATH')
        self.my_logger = my_logger

    def _get_file(self):
        return self.last_entry_file_path

    def save(self, last_board_message):
        with open(self._get_file(), 'wb') as last_board_message_file:
            pickle.dump(last_board_message, last_board_message_file)

    def get_message(self):
        try:
            with open(self._get_file(), 'rb') as last_board_message_file:
                self.my_logger.info("Loading last board message...")
                return pickle.load(last_board_message_file)
        except Exception:
            self.my_logger.info("Load failed, taking None message")
            return None
