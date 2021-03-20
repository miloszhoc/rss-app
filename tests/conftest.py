import tempfile
import pytest
from rss_app import create_app


@pytest.fixture()
def get_app():
    return create_app('test')


@pytest.fixture
def client(get_app):
    return get_app.test_client()


@pytest.fixture
def database(get_app):
    db_fd, db_file = tempfile.mkstemp()
    get_app.config['DATABASE'] = db_file
    from rss_app.database.models import db

    with get_app.app_context():
        db.create_all()
        yield db
        db.drop_all()
