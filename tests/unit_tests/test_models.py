import pytest
from rss_app.database.models import Url


def test_new_http_url():
    address = Url('http://www.bbc.co.uk/music/genres/rockandindie/reviews.rss')
    assert 'http://www.bbc.co.uk/music/genres/rockandindie/reviews.rss' == address.url


def test_new_https_url():
    address = Url('https://www.bbc.co.uk/music/genres/rockandindie/reviews.rss')
    assert 'https://www.bbc.co.uk/music/genres/rockandindie/reviews.rss' == address.url


def test_add_non_url():
    with pytest.raises(AssertionError):
        Url('bbc.co.uk/music/genres/rockandindie/reviews.rss')


def test_add_empty_url():
    with pytest.raises(AssertionError):
        Url('')
