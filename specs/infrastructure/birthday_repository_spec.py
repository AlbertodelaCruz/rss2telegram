from doublex import Spy, when, ANY_ARG
from expects import expect, equal
from mamba import description, context, it, before
from freezegun import freeze_time

from infrastructure.birthday_repository import BirthdayRepository
from infrastructure.birthday_repository import YamlWrapper
from specs import object_mother


with description('Birthday repository', 'unit') as self:
    with context('getting birthdays'):
        with before.each:
            self.yaml_wrapper = Spy(YamlWrapper)
            self.birthday_repository = BirthdayRepository(self.yaml_wrapper)

        with context('having birthdays for today'):
            with it('returns list of names'):
                now = object_mother.now()
                day_month = now.strftime("%d/%m")

                with freeze_time(now):
                    when(self.yaml_wrapper).load(ANY_ARG).returns({f'{day_month}': ['Alberto']})
                    result = self.birthday_repository.get_birthdays_for(now)

                    expect(result).to(equal(['Alberto']))

        with context('NO having birthdays for today'):
            with it('returns empty list'):
                now = object_mother.now()

                with freeze_time(now):
                    when(self.yaml_wrapper).load(ANY_ARG).returns({})
                    result = self.birthday_repository.get_birthdays_for(now)

                    expect(result).to(equal([]))
