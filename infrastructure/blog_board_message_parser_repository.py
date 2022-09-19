from bs4 import BeautifulSoup

from model.board_message_parser_repository import BoardMessageParserRepository


class BlogBoardMessageParserRepository(BoardMessageParserRepository):
    def __init__(self, requester):
        self._requester = requester

    def get_message(self, url):
        html = self._requester.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        if messages := soup.find_all("div", class_="et_pb_text_inner"):
            messages_with_content = [message for message in messages if 'Últimas entradas' not in message.get_text()]
            return messages_with_content[0].get_text() if messages_with_content else None
