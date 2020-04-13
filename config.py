import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# email data
SENDGRID_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL')

# database access
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_TABLE = os.environ.get('DB_TABLE')
DB_PORT = os.environ.get('DB_PORT')
DB_URL = 'postgresql+psycopg2://{user}:{passwd}@{url}:{port}/{db}'.format(user=DB_USER,
                                                                          passwd=DB_PASS,
                                                                          url=DB_HOST,
                                                                          port=DB_PORT,
                                                                          db=DB_NAME)
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 50,
    'max_overflow': 100}

db = SQLAlchemy(app, engine_options=SQLALCHEMY_ENGINE_OPTIONS)
ma = Marshmallow(app)

migrate = Migrate(app, db)
