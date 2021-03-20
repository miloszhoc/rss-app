import feedparser
import dominate
from dominate.tags import *
from dominate.util import text


# take raw DB response and yield urls
def get_urls(data: list):
    """
    :param data - DB rows data dump
    """
    if not data[0]:
        raise AssertionError('No urls')
    for d in data:
        yield d['url']


def parse_rss(url):
    if not url:
        raise AssertionError('Empty url')
    data = dict()
    parser = feedparser.parse(url)

    data['feed_title'] = parser.feed.title
    data['content'] = []

    for i in parser.entries:
        if i.has_key('summary'):
            data['content'].append(
                {'title': i.title, 'inside_content': {'text': i.summary, 'link': i.links[0].href}})
    return data


def create_html(data: dict):
    doc = dominate.document(title='RSS')
    with doc:
        for k, v in data.items():
            h1(v['feed_title'])
            for i in v['content']:
                p(i['title'], style='font-weight: bold;')
                text(i['inside_content']['text'])
                br()
                a('Read more', href=i['inside_content']['link'])
                br()
                br()
    return doc
