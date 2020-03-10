import feedparser
import dominate
from dominate.tags import *
from dominate.util import text


# take response and yield urls (without url id)
def get_urls(data):
    for d in data:
        yield d['url']


def parse_rss(url):
    data = dict()
    parser = feedparser.parse(url)
    feed_title = parser['feed']['title']

    data['feed_title'] = feed_title
    data['content'] = []

    [data['content'].append({'title': i['title'],
                             'inside_content': {'text': i['summary'], 'link': i['links'][0]['href']}})
     for i in parser['entries']]
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

