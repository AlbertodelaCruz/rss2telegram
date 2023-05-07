from doublex import Spy, when, ANY_ARG
from expects import expect, equal
from mamba import description, context, it, before
from freezegun import freeze_time

from model.birthday_service import BirthdayService
from specs import object_mother

with description('Birthday service', 'unit') as self:
    with context('getting publications'):
        with before.each:
            self.birthday_repository = Spy()
            self.birthday_service = BirthdayService(self.birthday_repository)

        with context('having birthdays for today'):
            with context('and it is 8 in the morning'):
                with it('returns new publications'):
                    one_day_at_8 = object_mother.one_day_at_8()
                    with freeze_time(one_day_at_8):
                        when(self.birthday_repository).get_birthdays_for(one_day_at_8).returns(['a_name', 'another_name'])
                        a_publication = object_mother.a_publication(date=one_day_at_8, title='Feliz cumpleaños a_name', content='🥳 🎉 👏')
                        another_publication = object_mother.a_publication(date=one_day_at_8, title='Feliz cumpleaños another_name', content='🥳 🎉 👏')

                        result = self.birthday_service.get_new_publications()

                        expect(result).to(equal([a_publication, another_publication]))

            with context('but already sent'):
                with it('returns empty list'):
                    one_day_at_8 = object_mother.one_day_at_8()
                    with freeze_time(one_day_at_8):
                        when(self.birthday_repository).get_birthdays_for(one_day_at_8).returns(['a_name'])
                        a_publication = object_mother.a_publication(date=one_day_at_8, title='Feliz cumpleaños a_name', content='🥳 🎉 👏')

                        self.birthday_service.get_new_publications()
                        result = self.birthday_service.get_new_publications()

                        expect(result).to(equal([]))

        with context('having no birthday'):
            with it('returns empty list of publications'):
                one_day_at_8 = object_mother.one_day_at_8()
                with freeze_time(one_day_at_8):
                    when(self.birthday_repository).get_birthdays_for(one_day_at_8).returns([])

                    result = self.birthday_service.get_new_publications()

                    expect(result).to(equal([]))
