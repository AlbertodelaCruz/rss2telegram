from mamba import description, context, it, before
from doublex import Spy, when, ANY_ARG
from expects import expect, equal

from dotenv import load_dotenv
import os
from datetime import datetime

from specs import object_mother

from factory import EnvLoader
from infrastructure.twitter import Twitter


with description('Feeder service') as self:
    with context('getting new entries'):
        with before.each:
            env_loader = Spy(EnvLoader)
            self.twitter_api = Spy()
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            self.twitter = Twitter(env_loader, self.twitter_api)

        with context('no tweets'):
            with it('returns saved datetime and empty list'):
                last_entry_datetime = object_mother.now()
                when(self.twitter_api).user_timeline(ANY_ARG).returns([])

                result = self.twitter.get_new_publications(last_entry_datetime)

                expect(result).to(equal((last_entry_datetime, [])))

        with context('having tweets'):
            with it('returns last published datetime and publication'):
                published_date = 'Thu Apr 06 15:24:15 +0000 2027'
                published_entry = datetime.strptime(published_date, "%a %b %d %H:%M:%S %z %Y")
                a_publication = object_mother.a_publication(date=published_entry, title='')
                a_tweet = object_mother.a_tweet(published_date)
                when(self.twitter_api).user_timeline(ANY_ARG).returns([a_tweet])
                last_entry_datetime = object_mother.now()

                result = self.twitter.get_new_publications(last_entry_datetime)

                expect(result).to(equal((published_entry, [a_publication])))