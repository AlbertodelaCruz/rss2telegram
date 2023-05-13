from datetime import datetime
import pytz

from model.publication.publication import Publication


class BirthdayService:
    def __init__(self, birthday_repository):
        self._birthday_repository = birthday_repository
        self._sent_for_today = False

    def get_new_publications(self):
        now = datetime.now()
        publications = []
        if now.hour == 7:
            self._sent_for_today = False
        if not self._sent_for_today and now.hour == 8:
            birthday_names = self._birthday_repository.get_birthdays_for(now)
            for birthday_name in birthday_names:
                publications.append(Publication(date=now, title=f'Feliz cumpleaños {birthday_name}', content='🥳 🎉 👏'))
            self._sent_for_today = True
        return publications
