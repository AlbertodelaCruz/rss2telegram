from dotenv import load_dotenv
from doublex import Spy, when
from doublex_expects import have_been_called_with, have_been_called
from expects import expect, contain, have_keys
from mamba import description, context, it, before

from infrastructure.factory import EnvLoader
from infrastructure.request_wrapper import RequestsWrapper
from model.telegram_notifier_service import TelegramNotifierService
from specs import object_mother

with description('Telegram notifier service', 'unit') as self:
    with context('sending publications'):
        with before.each:
            env_loader = Spy(EnvLoader)
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            self.request_wrapper = Spy(RequestsWrapper)
            self.telegram_notifier_service = TelegramNotifierService(env_loader, self.request_wrapper)

        with it('sends them'):
            a_publication = object_mother.a_publication(date='a_date', title='a_title', content='a_content')
            another_publication = object_mother.a_publication(date='another_date', title='a_title', content='a_content')

            self.telegram_notifier_service.send_publications([a_publication, another_publication])

            expected_text = 'a_title: a_content'
            expect(self.request_wrapper.post).to(have_been_called.twice)
            expect(self.request_wrapper.post).to(have_been_called_with(contain('api.telegram.org'),
                                                                  json=have_keys(text=expected_text)))

        with context('with a empty title publication'):
            with it('sends it'):
                a_publication = object_mother.a_publication(date='a_date', title='', content='a_content')

                self.telegram_notifier_service.send_publications([a_publication])

                expected_text = 'a_content'
                expect(self.request_wrapper.post).to(have_been_called_with(contain('api.telegram.org'),
                                                                      json=have_keys(text=expected_text)))