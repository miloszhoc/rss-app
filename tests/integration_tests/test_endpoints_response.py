import pytest
from unittest import mock
from requests import Response


@pytest.fixture()
def add_url(client, database):
    resp = client.post('/urls', data={'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'},
                       follow_redirects=True)
    return resp.json


def test_get_urls(client, add_url):
    c = client.get('/urls')
    assert len(c.json) == 1


def test_add_duplicated_url(client, database):
    resp = client.post('/urls', data={'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'},
                       follow_redirects=True)
    assert resp.json['success'] == True
    resp = client.post('/urls', data={'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'},
                       follow_redirects=True)
    assert resp.json['success'] == False
    assert resp.json['error'] == 'url already exists'


def test_add_non_url_address(client, database):
    resp = client.post('/urls', data={'url': 'aaaaaa'},
                       follow_redirects=True)
    assert resp.json['success'] == False
    assert 'This is not an URL address' in resp.json['error']


def test_delete_existing_url(client, add_url):
    url_id = add_url['data']['id']
    r = client.delete('/urls/' + str(url_id))
    assert r.json['success'] == True


def test_delete_not_existing_url(client):
    r = client.delete('/urls/23')
    assert 'element does not exist' in r.json['error']


def test_update_not_existing_url(client, add_url):
    id_url = add_url['data']['id']
    r = client.put('/urls/' + str(id_url), data={'url': 'http://www.bbc22.co.uk/music/genres/world/reviews.rss'})
    assert r.json['success'] == True
    assert r.json['data']['new_url'] == 'http://www.bbc22.co.uk/music/genres/world/reviews.rss'


def test_update_not_url(client, add_url):
    id_url = add_url['data']['id']
    r = client.put('/urls/' + str(id_url), data={'url': 'music/genres/world/reviews.rss'})
    assert r.json['success'] == False
    assert 'This is not an URL address' in r.json['error']


def test_update_empty_url(client, add_url):
    id_url = add_url['data']['id']
    r = client.put('/urls/' + str(id_url), data={'url': ''})
    assert r.json['success'] == False
    assert 'Empty address' in r.json['error']


def test_update_url_to_already_existing(client, add_url):
    id_url = add_url['data']['id']
    r = client.put('/urls/' + str(id_url), data={'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'})
    assert r.json['success'] == True


def test_get_rss(client, database):
    client.post('/urls', data={'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'})
    client.post('/urls', data={'url': 'https://www.polsatsport.pl/rss/pilkanozna.xml'},
                follow_redirects=True)
    r = client.get('/rss')
    assert r.json['success'] == True
    assert r.json['error'] == ''
    assert len(r.json['rss_content']) == 2


def test_get_non_rss(client, database):
    client.post('/urls', data={'url': 'https://www.youtube.com'})
    r = client.get('/rss')
    assert r.json['success'] == False
    assert r.json['error'] == 'One of URLS is not RSS'
    assert len(r.json['rss_content']) == 0
