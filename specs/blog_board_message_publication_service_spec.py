import os
from datetime import datetime

from dotenv import load_dotenv
from doublex import Spy, when, ANY_ARG
from expects import expect, equal
from mamba import description, context, it, before
from freezegun import freeze_time

from factory import EnvLoader
from model.board_message_publication_service import BoardMessagePublicationService
from specs import object_mother

with description('Blog board message publication service', 'unit') as self:
    with context('getting new messages'):
        with before.each:
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            self.blog_board_parser_repository = Spy()
            self.blog_board_message_publication_service = BoardMessagePublicationService(env_loader, self.blog_board_parser_repository)

        with context('new message'):
            with it('returns new message and the publication'):
                last_entry_datetime = object_mother.now()
                with freeze_time(last_entry_datetime):
                    now = object_mother.now()
                    when(self.blog_board_parser_repository).get_message(ANY_ARG).returns('a message')
                    a_publication = object_mother.a_publication(date=now, title='Nueva entrada en el tablón', content='a message')

                    result = self.blog_board_message_publication_service.get_new_publications('old message')

                    expect(result).to(equal(('a message', [a_publication])))

        with context('no new message'):
            with it('returns old message and empty list of publications'):
                when(self.blog_board_parser_repository).get_message(ANY_ARG).returns(None)

                result = self.blog_board_message_publication_service.get_new_publications('old message')

                expect(result).to(equal(('old message', [])))
