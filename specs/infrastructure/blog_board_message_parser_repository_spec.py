import os
from dotenv import load_dotenv
from mamba import description, context, it
from doublex import Spy, when, ANY_ARG
from expects import expect, equal, be_none

from infrastructure.factory import EnvLoader
from infrastructure.blog_board_message_parser_repository import BlogBoardMessageParserRepository
from specs.object_mother import FakeHTMLResponse, FakeHTMLNoMessageResponse


with description('Blog board message parser repository', 'unit') as self:
    with context('querying blog url'):
        with context('with a message at board'):
            with it('returns table message'):
                env_loader = Spy(EnvLoader)
                requester = Spy()
                when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
                when(requester).urlopen(ANY_ARG).returns(FakeHTMLResponse())
                self.blog_url = os.getenv('BLOG_TABLE_URL')
                self.blog_board_message_parser = BlogBoardMessageParserRepository(requester)

                result = self.blog_board_message_parser.get_message(self.blog_url)

                expect(result).to(equal('Necesitamos un paquete de toallitas para el lunes 12. Gracias.'))

        with context('with no message at board'):
            with it('returns None'):
                env_loader = Spy(EnvLoader)
                requester = Spy()
                when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
                when(requester).urlopen(ANY_ARG).returns(FakeHTMLNoMessageResponse())
                self.blog_url = os.getenv('BLOG_TABLE_URL')
                self.blog_board_message_parser = BlogBoardMessageParserRepository(requester)

                result = self.blog_board_message_parser.get_message(self.blog_url)

                expect(result).to(be_none)
