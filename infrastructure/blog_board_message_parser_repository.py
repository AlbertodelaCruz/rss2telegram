from bs4 import BeautifulSoup
import urllib

from model.board_message_parser_repository import BoardMessageParserRepository


class BlogBoardMessageParserRepository(BoardMessageParserRepository):
    def get_message(self, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        messages = soup.find_all("div", class_="et_pb_text_inner")
        if messages:
            return messages[0].get_text()
