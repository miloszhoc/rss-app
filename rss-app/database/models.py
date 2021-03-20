from . import db, ma
from sqlalchemy.orm import validates


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, url):
        self.url = url

    @validates('url')
    def validate_url(self, key, url):
        assert 'http://' in url or 'https://' in url
        return url


class UrlSchema(ma.Schema):
    class Meta:
        model = Url
        session = db.session
        fields = ('url', 'id')
