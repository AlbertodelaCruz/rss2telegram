import os
from datetime import datetime

from model.publication.publication import Publication


class BlogPublicationService():
    def __init__(self, env_loader, blog_parser_repository):
        env_loader.load_dotenv()
        self.blog_url = os.getenv('BLOG_URL')
        self.feed_tags = os.getenv('FEED_TAGS').split(',')
        self.blog_parser_repository = blog_parser_repository

    def get_new_publications(self, old_messages_datetime):
        feed = self.blog_parser_repository.parse(self.blog_url)
        entries = feed['entries']
        sorted_entries = sorted(entries, key=lambda d: d['published'])
        publications = []
        for entry in sorted_entries:
            old_messages_datetime, publications = self._append_new_publications(entry, publications, old_messages_datetime)
        return old_messages_datetime, publications

    def _append_new_publications(self, entry, publications, old_messages_datetime):
        published_time = datetime.strptime(entry['published'], "%a, %d %b %Y %H:%M:%S %z")
        if published_time > old_messages_datetime:
            for feed_tag_permitted in self.feed_tags:
                if feed_tag_permitted in entry['tags'][0].values():
                    old_messages_datetime = published_time
                    publication = Publication(date=published_time, title=entry['title'], content=entry['link'])
                    publications.append(publication)
        return old_messages_datetime, publications