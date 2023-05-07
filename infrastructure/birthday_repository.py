import yaml
import os


class BirthdayRepository:
    def __init__(self, yaml_wrapper):
        self.yaml_wrapper = yaml_wrapper

    def get_birthdays_for(self, time):
        day_month = time.strftime("%d/%m")
        yaml_data = self.yaml_wrapper.load()
        try:
            return yaml_data[day_month]
        except KeyError:
            return []


class YamlWrapper:
    def load(self):
        with open(os.getenv('BIRTHDAY_FILE'), "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
