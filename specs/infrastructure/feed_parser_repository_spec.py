import os
import feedparser
from dotenv import load_dotenv
from mamba import description, context, it
from doublex import Spy, when
from expects import expect, have_keys

from factory import EnvLoader
from infrastructure.feed_parser_repository import FeedParserRepository


with description('Feed parser repository', 'integration') as self:
    with context('querying blog url'):
        with it('returns entries'):
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            self.blog_url = os.getenv('BLOG_URL')
            self.feed_parser = FeedParserRepository(feedparser)

            result = self.feed_parser.parse(self.blog_url)

            expect(result).to(have_keys('entries'))
