import pytest
from sqlalchemy.orm.exc import ObjectDeletedError

from rss_app.database import models


@pytest.fixture()
def insert_url(client, database):
    url = 'http://feeds.bbci.co.uk/news/england/london/rss.xml'
    new_url = models.Url(url)
    database.session.add(new_url)
    database.session.commit()
    return new_url


def test_add_url(client, database):
    client.post('/urls', data={'url': 'http://www.bbc.co.uk/music/genres/world/reviews.rss'},
                follow_redirects=True)
    assert len(models.Url.query.all()) == 1


def test_delete_url(client, insert_url):
    url_id = insert_url.id
    client.delete('/urls/' + str(url_id))
    with pytest.raises(ObjectDeletedError):
        insert_url.url
    assert not len(models.Url.query.all())


def test_update_url(client, insert_url):
    id_url = insert_url.id
    assert models.Url.query.filter_by().first().url == insert_url.url

    new_url = 'http://www.bbc22.co.uk/music/genres/world/reviews.rss'
    client.put('/urls/' + str(id_url), data={'url': new_url})
    assert models.Url.query.filter_by().first().url == new_url
