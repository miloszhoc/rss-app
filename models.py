from config import db, ma


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, url):
        self.url = url


class UrlSchema(ma.ModelSchema):
    class Meta:
        model = Url
        session = db.session
        fields = ('url', 'id')
