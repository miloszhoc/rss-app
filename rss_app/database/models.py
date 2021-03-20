from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import validates

db = SQLAlchemy()
ma = Marshmallow()


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, url):
        self.url = url

    @validates('url')
    def validate_url(self, key, url):
        if url == '':
            raise AssertionError('Empty address')
        else:
            pass

        if 'http://' in url or 'https://' in url:
            pass
        else:
            raise AssertionError('This is not an URL address')
        return url


class UrlSchema(ma.Schema):
    class Meta:
        model = Url
        session = db.session
        fields = ('url', 'id')
