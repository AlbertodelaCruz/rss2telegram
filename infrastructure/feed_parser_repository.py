from model.blog_parser_repository import BlogParserRepository


class FeedParserRepository(BlogParserRepository):
    def __init__(self, parser):
        self._parser = parser

    def parse(self, url):
        return self._parser.parse(url)