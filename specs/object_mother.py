from datetime import datetime

import pytz

from model.publication.publication import Publication

A_TITLE = '¡Feliz fin de semana de Halloween!'
A_CONTENT = 'https://foo.com/2021/10/29/feliz-fin-de-semana-de-halloween/'


def now():
    return datetime.now(pytz.utc)

def a_feed(author, custom_tag, published):
    return dict(title=A_TITLE, title_detail={'type': 'text/plain', 'language': None, 'base': 'https://foo.com/feed/',
                                             'value': '¡Feliz fin de semana de Halloween!'}, links=[
        {'rel': 'alternate', 'type': 'text/html',
         'href': 'https://foo.com/2021/10/29/feliz-fin-de-semana-de-halloween/'}],
                link=A_CONTENT, authors=[{'email': author}],
                author=author, author_detail={'email': author}, published=published,
                published_parsed='time.struct_time(tm_year=2021, tm_mon=10, tm_mday=29, tm_hour=13, tm_min=6, tm_sec=57, tm_wday=4, tm_yday=302, tm_isdst=0)',
                tags=[{'term': custom_tag, 'scheme': None, 'label': None}], id='https://foo.com/?p=51520',
                guidislink=False,
                summary='¡Hola chic@s! Para este puente, os dejamos unas actividades horripilantemente [&#8230;]',
                summary_detail={'type': 'text/html', 'language': None, 'base': 'https://foo.com/feed/',
                                'value': '¡Hola chic@s! Para este puente, os dejamos unas actividades horripilantemente [&#8230;]'},
                content=[{'type': 'text/html', 'language': None, 'base': 'https://foo.com/feed/',
                          'value': '<h1 style="text-align: center;"><span style="color: #ff6600;">¡Hola chic@s!</span></h1>\n<h1 style="text-align: center;"></h1>\n<h1 style="text-align: center;"><span style="color: #800080;">Para este puente, os dejamos unas actividades horripilantemente divertidas.</span></h1>\n<p><a href="https://foo.com/wp-content/uploads/2021/10/DOSSIER-HALLOWEEN-TERRORÍFICO-@aliciapaisdemaravillas-@the.teachersbag-@teacher_carmen_pt.pdf">DOSSIER HALLOWEEN TERRORÍFICO </a></p>\n<h1 style="text-align: center;"><span style="color: #ff6600;">¡Disfrutad mucho de la fiesta de Halloween y que os lo paséis terriblemente bien!</span></h1>\n<p>&nbsp;</p>\n<p><img alt="Fotomural Alicia en el País de las Maravillas – Grafidecor" src="https://grafidecor.es/wp-content/uploads/2019/10/FOTOMURAL-14-PAISAJE-INFANTIL-ALICIA-PAIS-MARAVILLAS-1.jpg" /></p>'}])

def a_tweet(date):
    return Tweet(date)

def a_publication(date, title=A_TITLE, content=A_CONTENT):
    return Publication(date=date,title=title, content=content)

def a_blog_board_html_response():
    return b'<!DOCTYPE html>\n<html lang="es">\n<head>\n\t<meta charset="UTF-8" />\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n\t<link rel="pingback" href="https://blogshumanitastorrejon.com/xmlrpc.php" />\n\n\t<script type="text/javascript">\n\t\tdocument.documentElement.className = \'js\';\n\t</script>\n\n\t<title>Blog de 2.\xc2\xba de infantil (4 a\xc3\xb1os) | Blogs del Colegio Humanitas Torrej\xc3\xb3n</title><div class="et_pb_module et_pb_text et_pb_text_0  et_pb_text_align_left et_pb_bg_layout_light">\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t<div class="et_pb_text_inner"><p>Necesitamos un paquete de toallitas para el lunes 12. Gracias.</p></div><div class="et_pb_text_inner"><h2>\xc3\x9altimas entradas</h2></div>\n\t\t\t</div>\n\t\t\t</div></body>\n</html>'

def a_blog_board_html_response_with_no_content():
    return b'<!DOCTYPE html>\n<html lang="es">\n<head>\n\t<meta charset="UTF-8" />\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n\t<link rel="pingback" href="https://blogshumanitastorrejon.com/xmlrpc.php" />\n\n\t<script type="text/javascript">\n\t\tdocument.documentElement.className = \'js\';\n\t</script>\n\n\t<title>Blog de 2.\xc2\xba de infantil (4 a\xc3\xb1os) | Blogs del Colegio Humanitas Torrej\xc3\xb3n</title><div class="et_pb_module et_pb_text et_pb_text_0  et_pb_text_align_left et_pb_bg_layout_light">\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t<div class="et_pb_text_inner"><h2>\xc3\x9altimas entradas</h2></div>\n\t\t\t</div>\n\t\t\t</div></body>\n</html>'


class Tweet:
    def __init__(self, date):
        self._json = {'created_at': date,
                      'text': A_CONTENT}


class FakeHTMLResponse:
    def read(self):
        return a_blog_board_html_response()


class FakeHTMLNoMessageResponse:
    def read(self):
        return a_blog_board_html_response_with_no_content()
