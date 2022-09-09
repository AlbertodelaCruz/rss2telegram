from datetime import datetime

import feedparser
import pytz
from dotenv import load_dotenv
from doublex import Spy, when
from expects import expect, raise_error
from mamba import description, context, it

from factory import EnvLoader, TwitterAPI, request_wrapper, blog_board_message_parser_repository
from infrastructure.last_publication_file_retriever import LastPublicationFileRetriever
from model.blog_publication_service import BlogPublicationService
from model.telegram_notifier_service import TelegramNotifierService
from model.twitter_publication_service import TwitterPublicationService
from model.board_message_publication_service import BoardMessagePublicationService
from infrastructure.last_board_message_file_service import LastBoardMessageFileService
from use_case.send_new_publications import SendNewPublications

with description('App rss_to_telegram', 'acceptance'):
    with context('running the service'):
        with it('executes and finish correctly'):
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            my_logger = Spy()
            twitter_client = TwitterAPI(env_loader)
            last_entry_datetimes = {'feed': datetime.now(pytz.utc), 'twitter': datetime.now(pytz.utc)}
            twitter = TwitterPublicationService(env_loader, twitter_client)
            feeder = BlogPublicationService(env_loader, feedparser)
            last_entry_service = LastPublicationFileRetriever(env_loader, my_logger)
            telegram_notifier_service = TelegramNotifierService(env_loader, request_wrapper())
            board_message_service = BoardMessagePublicationService(env_loader, blog_board_message_parser_repository())
            last_board_message_file_service = LastBoardMessageFileService(env_loader, my_logger)
            self.send_new_entries_use_case = SendNewPublications(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes, telegram_notifier_service, board_message_service, last_board_message_file_service)

            def executes_program_does_not_raise_error():
                try:
                    self.send_new_entries_use_case.send()
                except Exception as exc:
                    import traceback
                    print(traceback.print_exc())
                    raise exc

            expect(executes_program_does_not_raise_error).not_to(raise_error(Exception))
