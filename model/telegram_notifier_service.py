import os


class TelegramNotifierService:
    def __init__(self, env_loader, requests_wrapper):
        env_loader.load_dotenv()
        self.requests_wrapper = requests_wrapper
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot_chatID = os.getenv('BOT_CHATID')

    def send_publications(self, publications):
        for publication in publications:
            text = f"{publication.title}: {publication.content}" if publication.title != '' else f"{publication.content}"
            telegram_body = {'chat_id':f'{self.bot_chatID}', 'parse_mode':'Markdown', 'text':f"{text}"}
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            _ = self.requests_wrapper.post(url, json=telegram_body)