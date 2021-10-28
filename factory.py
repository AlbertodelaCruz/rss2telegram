from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime
import requests


class EnvLoader:
    def load_dotenv(self):
        dotenv_path = Path('./system/.env.test')
        load_dotenv(dotenv_path=dotenv_path)
