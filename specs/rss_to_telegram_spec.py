from mamba import description, context, it, before
from doublex import Spy, when, ANY_ARG
from expects import expect, raise_error
from doublex_expects import have_been_called_with

from dotenv import load_dotenv

from rss_2_telegram import main
from factory import EnvLoader
from twitter import Twitter
from feeder import Feeder

with description('App rss_to_telegram'):
    with context('running the service'):
        with before.each:
            self.my_logger = Spy()
            self.last_entry_service = Spy()
            self.twitter = Spy(Twitter)
            self.feeder = Spy(Feeder)
            self.a_datetime = 'a_datetime'
            self.last_entry_datetimes = {'feed': self.a_datetime, 'twitter': self.a_datetime}
            self.a_feed_entry = {'title': 'a_title'}
            self.a_twitter_entry = FakeTwitterEntry()
            when(self.feeder).get_new_entries(ANY_ARG).returns(('a_date', [self.a_feed_entry]))
            when(self.twitter).get_new_entries(ANY_ARG).returns(('a_date', [self.a_twitter_entry]))
            when(self.last_entry_service).get_file(ANY_ARG).returns('/dev/null')

        with it('retrieves new feeds'):
            main(self.my_logger, self.last_entry_service, self.twitter, self.feeder, self.last_entry_datetimes)

            expect(self.feeder.get_new_entries).to(have_been_called_with(self.a_datetime))

        with it('retrieves new tweets'):
            main(self.my_logger, self.last_entry_service, self.twitter, self.feeder, self.last_entry_datetimes)

            expect(self.twitter.get_new_entries).to(have_been_called_with(self.a_datetime))

        with it('sends to telegram new feeds'):
            main(self.my_logger, self.last_entry_service, self.twitter, self.feeder, self.last_entry_datetimes)

            expect(self.feeder.send_entries).to(have_been_called_with([self.a_feed_entry]))

        with it('sends to telegram new tweets'):
            main(self.my_logger, self.last_entry_service, self.twitter, self.feeder, self.last_entry_datetimes)

            expect(self.twitter.send_entries).to(have_been_called_with([self.a_twitter_entry]))


class FakeTwitterEntry():
    def __init__(self):
        self._json = {'text': 'a_text'}
