from mamba import description, context, it
from doublex import Spy, when
from expects import expect, raise_error

from dotenv import load_dotenv

from rss_2_telegram import main
from factory import EnvLoader
from twitter import Twitter
from feeder import Feeder

with description('App rss_to_telegram'):
    with context('running the service'):
        with it('executes and finish correctly'):
            env_loader = Spy(EnvLoader)
            my_logger = Spy()
            twitter = Twitter(env_loader)
            feeder = Feeder(env_loader)

            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))

            def executes_program_does_not_raise_error():
                main(env_loader, my_logger, twitter, feeder)

            expect(executes_program_does_not_raise_error).not_to(raise_error(Exception))
