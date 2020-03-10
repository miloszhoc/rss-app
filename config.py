import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# email data
SENDGRID_KEY = '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'
FROM_EMAIL = 'mhoc_rss@cloud_app.com'

# local database access
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASS = 'licencjat123!'
DB_NAME = 'cloud_app_db'
DB_TABLE = 'url'
DB_PORT = '5432'

DB_URL = 'postgresql+psycopg2://{user}:{passwd}@{url}:{port}/{db}'.format(user=DB_USER,
                                                                          passwd=DB_PASS,
                                                                          url=DB_HOST,
                                                                          port=DB_PORT,
                                                                          db=DB_NAME)
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)
