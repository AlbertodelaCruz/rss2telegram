from mamba import description, context, it
from doublex import Spy, when
from expects import expect, equal

from dotenv import load_dotenv

from specs import object_mother

from factory import EnvLoader
from feeder import Feeder

with description('Feeder service'):
    with context('getting new entries'):
        with it('returns them and last feed datetime'):
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            feeder = Feeder(env_loader)
            last_entry_datetime = object_mother.now()

            result = feeder.get_new_entries(last_entry_datetime)

            expect(result).to(equal((last_entry_datetime, [])))
