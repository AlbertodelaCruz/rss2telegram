import os
from dotenv import load_dotenv
from mamba import description, context, it
from doublex import Spy, when
from expects import expect, be_none

from factory import EnvLoader
from infrastructure.blog_board_message_parser_repository import BlogBoardMessageParserRepository


with description('Blog board message parser repository', 'integration') as self:
    with context('querying blog url'):
        with it('returns table message'):
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            self.blog_url = os.getenv('BLOG_TABLE_URL')
            self.blog_board_message_parser = BlogBoardMessageParserRepository()

            result = self.blog_board_message_parser.get_message(self.blog_url)

            expect(result).not_to(be_none)
