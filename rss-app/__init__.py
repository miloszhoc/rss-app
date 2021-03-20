from flask import Flask, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 1000,
    'max_overflow': 2000}

db = SQLAlchemy(engine_options=SQLALCHEMY_ENGINE_OPTIONS)
ma = Marshmallow()


def create_app(config_name=None):
    from config import config_names
    app = Flask(__name__)
    app.config.from_object(config_names[config_name])
    cors = CORS()
    migrate = Migrate()

    ma.init_app(app)
    db.init_app(app)
    cors.init_app(app)

    migrate.init_app(app, db)

    @app.route('/is-alive')
    def is_alive():
        return jsonify(alive=True)

    return app
