from datetime import datetime
import requests
import os

import feedparser


class Feeder:
    def __init__(self, env_loader, feedparser):
        env_loader.load_dotenv()
        self.blog_url = os.getenv('BLOG_URL')
        self.feed_tags = os.getenv('FEED_TAGS').split(',')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot_chatID = os.getenv('BOT_CHATID')
        self.parser = feedparser

    def get_new_entries(self, old_messages_datetime):
        feed = self.parser.parse(self.blog_url)
        entries = feed['entries']
        sorted_entries = sorted(entries, key=lambda d: d['published'])
        new_entries = []
        for entry in sorted_entries:
            published_time = datetime.strptime(entry['published'], "%a, %d %b %Y %H:%M:%S %z" )
            if published_time > old_messages_datetime:
                for feed_tag_permitted in self.feed_tags:
                    if feed_tag_permitted in entry['tags'][0].values():
                        old_messages_datetime = published_time
                        new_entries.append(entry)
        return old_messages_datetime, new_entries

    def send_entries(self, entries):
        for entry in entries:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.bot_chatID}&parse_mode=Markdown&text={entry['title']}"
            _ = requests.get(url)
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.bot_chatID}&parse_mode=Markdown&text={entry['link']}"
            _ = requests.get(url)
