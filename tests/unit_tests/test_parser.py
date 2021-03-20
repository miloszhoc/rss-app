import pytest
from rss_app.rss_parser import get_urls, parse_rss, create_html
from unittest.mock import create_autospec
from requests import Response


@pytest.mark.parametrize('test_input, expected',
                         [([{'id': 1, 'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'}],
                           ['http://www.bbc.co.uk/music/genres/world/reviews.rss']),
                          ([{'id': 1, 'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'},
                            {'id': 2, 'url': 'https://news.google.com/rss?topic=h&hl=pl&gl=PL&ceid=PL:pl'}],
                           ['http://www.bbc.co.uk/music/genres/world/reviews.rss',
                            'https://news.google.com/rss?topic=h&hl=pl&gl=PL&ceid=PL:pl'])])
def test_get_urls(test_input, expected):
    assert list(get_urls(test_input)) == expected


def test_get_empty_urls():
    with pytest.raises(AssertionError):
        list(get_urls([{}])) == []


def test_parse_rss():
    with open('tests/unit_tests/rss_parser_test_data.xml', 'br') as f:
        actual = parse_rss(f)
    expected = {'feed_title': 'Latest World Reviews',
                'content': [
                    {'title': 'Fela Kuti - The Best of the Black President 2', 'inside_content': {
                        'text': 'Cherry-picked cuts from the catalogue of He Who Carries Death In His Pouch.',
                        'link': 'http://www.bbc.co.uk/music/reviews/26b6'}},
                    {'title': 'Salif Keita - TalĂŠ',
                     'inside_content': {'text': 'A loveable enough effort from the Malian star.',
                                        'link': 'http://www.bbc.co.uk/music/reviews/vxwx'}},
                    {'title': 'Bomba EstĂŠreo - Elegancia Tropical', 'inside_content': {
                        'text': 'BogotĂĄ quintet delivers fiery electro-Cumbia contortions with hidden depths.',
                        'link': 'http://www.bbc.co.uk/music/reviews/qwgw'}}
                ]}
    assert actual == expected


def test_parse_empty_rss_url():
    with pytest.raises(AssertionError):
        parse_rss('')


def test_parse_not_rss():
    with pytest.raises(AttributeError):
        parse_rss('''<html>
        <head><title>Test</title></head>
        <body>
        Simple test.
        </body>
        </html>''')


def test_create_html():
    response = create_autospec(Response)
    response.json.return_value = {'error': '',
                                  'success': True,
                                  'rss_content': {
                                      'http://www.bbc.co.uk/music/genres/world/reviews.rss': {
                                          'feed_title': 'Latest World Reviews',
                                          'content': [
                                              {
                                                  'title': 'Fela Kuti - The Best of the Black President 2',
                                                  'inside_content': {
                                                      'text': 'Cherry-picked cuts from the catalogue of He Who Carries Death In His Pouch.',
                                                      'link': 'http://www.bbc.co.uk/music/reviews/26b6'}},
                                              {'title': 'Salif Keita - TalĂŠ',
                                               'inside_content': {
                                                   'text': 'A loveable enough effort from the Malian star.',
                                                   'link': 'http://www.bbc.co.uk/music/reviews/vxwx'}}
                                          ]},
                                      'https://www.polsatsport.pl/rss/pilkanozna.xml': {
                                          'feed_title': 'Polsat Sport - Wiadomości - Piłka nożna',
                                          'content': [
                                              {
                                                  'title': 'Serie A: Koronawirus w Interze! Mecz z Sassuolo ma być przełożony',
                                                  'inside_content': {
                                                      'text': 'Sobotni mecz ligowy Interu u siebie z Sassuolo ma zostać przełożony, a piłkarze lidera włoskiej ekstraklasy zostaną wycofani z reprezentacji swoich krajów, po dwóch kolejnych przypadkach COVID-19 w drużynie - oświadczył klub z Mediolanu.',
                                                      'link': 'https://www.polsatsport.pl/wiadomosc/2021-03-18/serie-a-koronawirus-w-interze-mecz-z-sassuolo-ma-byc-przelozony/'}},
                                              {
                                                  'title': 'El. MŚ 2022: Holenderscy kibice w 30 minut wykupili dostępne bilety',
                                                  'inside_content': {
                                                      'text': 'Zaledwie 30 minut potrzebowali holenderscy kibice, aby wykupić pięć tysięcy biletów na mecz eliminacji piłkarskich mistrzostw świata z udziałem reprezentacji Holandii i Łotwy. Spotkanie odbędzie się 27 marca w Amsterdamie.',
                                                      'link': 'https://www.polsatsport.pl/wiadomosc/2021-03-18/el-ms-2022-holenderscy-kibice-w-30-minut-wykupili-dostepne-bilety/'}}
                                          ]}}}

    actual = create_html(response.json()['rss_content'])
    actual_content = actual.render()
    assert actual.title == 'RSS'
    assert 'Fela Kuti - The Best of the Black President 2' in actual_content
    assert 'A loveable enough effort from the Malian star.' in actual_content
    assert 'http://www.bbc.co.uk/music/reviews/26b6' in actual_content
