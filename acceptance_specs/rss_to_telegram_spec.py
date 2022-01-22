from mamba import description, context, it
from doublex import Spy, when
from expects import expect, raise_error

from dotenv import load_dotenv
from datetime import datetime
import pytz
import feedparser

from use_case.send_new_entries import SendNewEntries
from factory import EnvLoader
from infrastructure.twitter import Twitter
from infrastructure.blog import Blog
from last_entry_service import LastEntryService

with description('App rss_to_telegram'):
    with context('running the service'):
        with it('executes and finish correctly'):
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            my_logger = Spy()
            last_entry_datetimes = {'feed': datetime.now(pytz.utc), 'twitter': datetime.now(pytz.utc)}
            twitter = Twitter(env_loader)
            feeder = Blog(env_loader, feedparser)
            last_entry_service = LastEntryService(env_loader, my_logger)
            self.send_new_entries_use_case = SendNewEntries(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes)

            def executes_program_does_not_raise_error():
                self.send_new_entries_use_case.send()

            expect(executes_program_does_not_raise_error).not_to(raise_error(Exception))
