from mamba import description, context, it
from doublex import Spy, when
from expects import expect, raise_error

from dotenv import load_dotenv
from datetime import datetime
import pytz

from rss_2_telegram import main
from factory import EnvLoader
from twitter import Twitter
from feeder import Feeder
from last_entry_service import LastEntryService

with description('App rss_to_telegram'):
    with context('running the service'):
        with it('executes and finish correctly'):
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            my_logger = Spy()
            last_entry_datetimes = {'feed': datetime.now(pytz.utc), 'twitter': datetime.now(pytz.utc)}
            twitter = Twitter(env_loader)
            feeder = Feeder(env_loader)
            last_entry_service = LastEntryService(env_loader, my_logger)

            def executes_program_does_not_raise_error():
                main(my_logger, last_entry_service, twitter, feeder, last_entry_datetimes)

            expect(executes_program_does_not_raise_error).not_to(raise_error(Exception))
