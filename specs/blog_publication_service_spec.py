import os
from datetime import datetime

from dotenv import load_dotenv
from doublex import Spy, when, ANY_ARG
from expects import expect, equal
from mamba import description, context, it, before

from infrastructure.factory import EnvLoader
from model.blog_publication_service import BlogPublicationService
from specs import object_mother

with description('Blog publication service', 'unit') as self:
    with context('getting new publications'):
        with before.each:
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            self.blog_parser_repository = Spy()
            self.blog_publication_service = BlogPublicationService(env_loader, self.blog_parser_repository)
            self.published_date = 'Fri, 29 Oct 2022 13:06:57 +0000'
            self.published_entry = datetime.strptime(self.published_date, "%a, %d %b %Y %H:%M:%S %z")

        with context('no matching tags'):
            with it('returns saved datetime and empty list'):
                a_feed = object_mother.a_feed('an_author', 'a_custom_tag', self.published_date)
                when(self.blog_parser_repository).parse(ANY_ARG).returns({'entries': [a_feed]})
                last_entry_datetime = object_mother.now()

                result = self.blog_publication_service.get_new_publications(last_entry_datetime)

                expect(result).to(equal((last_entry_datetime, [])))

        with context('matching with env tag'):
            with it('returns last published datetime and publication'):
                tags_permitted = os.getenv('FEED_TAGS')
                a_tag_permitted = tags_permitted.split(',')[0]
                a_feed = object_mother.a_feed(os.getenv('FEED_AUTHOR'), a_tag_permitted, self.published_date)
                a_publication = object_mother.a_publication(date=self.published_entry)
                when(self.blog_parser_repository).parse(ANY_ARG).returns({'entries': [a_feed]})
                last_entry_datetime = object_mother.now()

                result = self.blog_publication_service.get_new_publications(last_entry_datetime)

                expect(result).to(equal((self.published_entry, [a_publication])))