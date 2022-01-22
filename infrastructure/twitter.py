from datetime import datetime
import requests
import os


from model.entry_service import EntryService
from model.publication.publication import Publication


class Twitter(EntryService):
    def __init__(self, env_loader, twitter_api):
        env_loader.load_dotenv()
        self.twitter_account = os.getenv('TWITTER_ACCOUNT')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot_chatID = os.getenv('BOT_CHATID')
        self._twitter_api = twitter_api

    def get_new_publications(self, old_messages_datetime):
        timeline = self._twitter_api.user_timeline(screen_name=self.twitter_account)
        new_publications = []
        for tweet in timeline:
            old_messages_datetime, new_publications = self._append_new_publications(tweet, new_publications, old_messages_datetime)
        return old_messages_datetime, new_publications

    def send_publications(self, publications):
        for publication in publications:
            telegram_body = {'chat_id':f'{self.bot_chatID}', 'parse_mode':'Markdown', 'text':f"{publication.content}"}
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            _ = requests.post(url, json=telegram_body)

    def _append_new_publications(self, tweet, new_publications, old_messages_datetime):
        published_time = datetime.strptime(tweet._json['created_at'], "%a %b %d %H:%M:%S %z %Y")
        if published_time > old_messages_datetime:
            old_messages_datetime = published_time
            publication = Publication(date=published_time, title='', content=tweet._json['text'])
            new_publications.append(publication)
        return old_messages_datetime, new_publications