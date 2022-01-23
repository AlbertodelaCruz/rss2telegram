import os
from datetime import datetime

from model.publication.publication import Publication


class TwitterPublicationService():
    def __init__(self, env_loader, twitter_api):
        env_loader.load_dotenv()
        self.twitter_account = os.getenv('TWITTER_ACCOUNT')
        self._twitter_api = twitter_api

    def get_new_publications(self, old_messages_datetime):
        timeline = self._twitter_api.user_timeline(screen_name=self.twitter_account)
        new_publications = []
        for tweet in timeline:
            old_messages_datetime, new_publications = self._append_new_publications(tweet, new_publications, old_messages_datetime)
        return old_messages_datetime, new_publications

    def _append_new_publications(self, tweet, new_publications, old_messages_datetime):
        published_time = datetime.strptime(tweet._json['created_at'], "%a %b %d %H:%M:%S %z %Y")
        if published_time > old_messages_datetime:
            old_messages_datetime = published_time
            publication = Publication(date=published_time, title='', content=tweet._json['text'])
            new_publications.append(publication)
        return old_messages_datetime, new_publications