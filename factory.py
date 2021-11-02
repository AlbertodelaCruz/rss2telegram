from dotenv import load_dotenv
from pathlib import Path
import logging
import logging.handlers


class EnvLoader:
    def load_dotenv(self):
        dotenv_path = Path('./system/.env')
        load_dotenv(dotenv_path=dotenv_path)

class Logger:
    @staticmethod
    def get_logger():
        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        my_logger.addHandler(handler)
        return my_logger
