from doublex import Spy, when, ANY_ARG
from doublex_expects import have_been_called_with
from expects import expect
from mamba import description, context, it, before

from model.blog_publication_service import BlogPublicationService
from model.board_message_publication_service import BoardMessagePublicationService
from model.telegram_notifier_service import TelegramNotifierService
from model.twitter_publication_service import TwitterPublicationService
from specs import object_mother
from use_case.send_new_publications import SendNewPublications

with description('App rss_to_telegram', 'unit') as self:
    with context('running the service'):
        with before.each:
            self.my_logger = Spy()
            self.last_entry_service = Spy()
            self.last_board_message_service = Spy()
            self.twitter_publication_service = Spy(TwitterPublicationService)
            self.blog_publication_service = Spy(BlogPublicationService)
            self.telegram_notifier_service = Spy(TelegramNotifierService)
            self.board_message_publication_service = Spy(BoardMessagePublicationService)
            self.a_datetime = 'a_datetime'
            self.last_entry_datetimes = {'feed': self.a_datetime, 'twitter': self.a_datetime}
            self.last_board_message = None
            self.a_feed_publication = object_mother.a_publication(date=self.a_datetime)
            self.a_twitter_publication = object_mother.a_publication(date=self.a_datetime)
            self.a_board_publication = object_mother.a_publication(date=self.a_datetime)

            self.send_new_entries_use_case = SendNewPublications(self.my_logger, self.last_entry_service, self.twitter_publication_service,
                                                                 self.blog_publication_service, self.last_entry_datetimes, self.telegram_notifier_service, self.board_message_publication_service, self.last_board_message_service)

            when(self.blog_publication_service).get_new_publications(ANY_ARG).returns(('a_date', [self.a_feed_publication]))
            when(self.twitter_publication_service).get_new_publications(ANY_ARG).returns(('a_date', [self.a_twitter_publication]))
            when(self.board_message_publication_service).get_new_publications(ANY_ARG).returns(('a_message', [self.a_board_publication]))

        with it('retrieves new feeds'):
            self.send_new_entries_use_case.send()

            expect(self.blog_publication_service.get_new_publications).to(have_been_called_with(self.a_datetime))

        with it('retrieves new tweets'):
            self.send_new_entries_use_case.send()

            expect(self.twitter_publication_service.get_new_publications).to(have_been_called_with(self.a_datetime))

        with it('retrieves new board message'):
            self.send_new_entries_use_case.send()

            expect(self.board_message_publication_service.get_new_publications).to(have_been_called_with(self.last_board_message))

        with it('sends to telegram new feeds'):
            self.send_new_entries_use_case.send()

            expect(self.telegram_notifier_service.send_publications).to(have_been_called_with([self.a_feed_publication]))

        with it('sends to telegram new tweets'):
            self.send_new_entries_use_case.send()

            expect(self.telegram_notifier_service.send_publications).to(have_been_called_with([self.a_twitter_publication]))

        with it('sends to telegram new board message'):
            self.send_new_entries_use_case.send()

            expect(self.telegram_notifier_service.send_publications).to(have_been_called_with([self.a_board_publication]))

