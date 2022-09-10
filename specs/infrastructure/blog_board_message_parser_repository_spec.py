import os
from dotenv import load_dotenv
from mamba import description, context, it
from doublex import Spy, when, ANY_ARG
from expects import expect, equal

from factory import EnvLoader
from infrastructure.blog_board_message_parser_repository import BlogBoardMessageParserRepository
from specs.object_mother import FakeHTMLResponse


with description('Blog board message parser repository', 'unit') as self:
    with context('querying blog url'):
        with it('returns table message'):
            env_loader = Spy(EnvLoader)
            requester = Spy()
            when(env_loader).load_dotenv().returns(load_dotenv('./system/.env.test'))
            when(requester).urlopen(ANY_ARG).returns(FakeHTMLResponse())
            self.blog_url = os.getenv('BLOG_TABLE_URL')
            self.blog_board_message_parser = BlogBoardMessageParserRepository(requester)

            result = self.blog_board_message_parser.get_message(self.blog_url)

            expect(result).to(equal('Necesitamos un paquete de toallitas para el lunes 12. Gracias.'))


def a_byte_response():
    return b'<!DOCTYPE html>\n<html lang="es">\n<head>\n\t<meta charset="UTF-8" />\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n\t<link rel="pingback" href="https://blogshumanitastorrejon.com/xmlrpc.php" />\n\n\t<script type="text/javascript">\n\t\tdocument.documentElement.className = \'js\';\n\t</script>\n\n\t<title>Blog de 2.\xc2\xba de infantil (4 a\xc3\xb1os) | Blogs del Colegio Humanitas Torrej\xc3\xb3n</title><div class="et_pb_module et_pb_text et_pb_text_0  et_pb_text_align_left et_pb_bg_layout_light">\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t<div class="et_pb_text_inner"><p>Necesitamos un paquete de toallitas para el lunes 12. Gracias.</p></div>\n\t\t\t</div>\n\t\t\t</div></body>\n</html>'