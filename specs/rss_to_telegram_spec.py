from doublex import Spy, when, ANY_ARG
from doublex_expects import have_been_called_with
from expects import expect
from mamba import description, context, it, before

from model.blog_publication_service import BlogPublicationService
from model.telegram_notifier_service import TelegramNotifierService
from model.twitter_publication_service import TwitterPublicationService
from specs import object_mother
from use_case.send_new_publications import SendNewPublications

with description('App rss_to_telegram', 'unit') as self:
    with context('running the service'):
        with before.each:
            self.my_logger = Spy()
            self.last_entry_service = Spy()
            self.twitter_publication_service = Spy(TwitterPublicationService)
            self.blog_publication_service = Spy(BlogPublicationService)
            self.telegram_notifier_service = Spy(TelegramNotifierService)
            self.a_datetime = 'a_datetime'
            self.last_entry_datetimes = {'feed': self.a_datetime, 'twitter': self.a_datetime}
            self.a_feed_publication = object_mother.a_publication(date=self.a_datetime)
            self.a_twitter_publication = object_mother.a_publication(date=self.a_datetime)

            self.send_new_entries_use_case = SendNewPublications(self.my_logger, self.last_entry_service, self.twitter_publication_service,
                                                                 self.blog_publication_service, self.last_entry_datetimes, self.telegram_notifier_service)

            when(self.blog_publication_service).get_new_publications(ANY_ARG).returns(('a_date', [self.a_feed_publication]))
            when(self.twitter_publication_service).get_new_publications(ANY_ARG).returns(('a_date', [self.a_twitter_publication]))
            when(self.last_entry_service).get_file(ANY_ARG).returns('/dev/null')



        with it('retrieves new feeds'):
            self.send_new_entries_use_case.send()

            expect(self.blog_publication_service.get_new_publications).to(have_been_called_with(self.a_datetime))

        with it('retrieves new tweets'):
            self.send_new_entries_use_case.send()

            expect(self.twitter_publication_service.get_new_publications).to(have_been_called_with(self.a_datetime))

        with it('sends to telegram new feeds'):
            self.send_new_entries_use_case.send()

            expect(self.telegram_notifier_service.send_publications).to(have_been_called_with([self.a_feed_publication]))

        with it('sends to telegram new tweets'):
            self.send_new_entries_use_case.send()

            expect(self.telegram_notifier_service.send_publications).to(have_been_called_with([self.a_twitter_publication]))

