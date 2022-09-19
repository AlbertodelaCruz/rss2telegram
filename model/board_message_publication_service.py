import os
from datetime import datetime
import pytz

from model.publication.publication import Publication


class BoardMessagePublicationService():
    def __init__(self, env_loader, blog_table_parser_repository):
        env_loader.load_dotenv()
        self.blog_url = os.getenv('BLOG_TABLE_URL')
        self.blog_table_parser_repository = blog_table_parser_repository

    def get_new_publications(self, old_message):
        message = self.blog_table_parser_repository.get_message(self.blog_url)
        if message and message != old_message:
            now = datetime.now(pytz.utc)
            publication = Publication(date=now, title='Nueva entrada en el tablón (https://blogshumanitastorrejon.com/blog-de-2o-de-infantil-4-anos/) 📋 ⬇️️', content=message)
            return message, [publication]
        return old_message, []
