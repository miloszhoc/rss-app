from rss_app.application import bp


def create_app(config_name=None, **kwargs):
    from flask import Flask, jsonify
    from flask_cors import CORS
    from flask_migrate import Migrate
    from rss_app.database.models import ma, db
    from rss_app.config import config_names

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_names[config_name if config_name else 'dev'])

    cors = CORS()
    migrate = Migrate()

    ma.init_app(app)
    db.init_app(app)
    cors.init_app(app)

    migrate.init_app(app, db)

    @app.route('/is-alive')
    def is_alive():
        return jsonify(alive=True)

    app.register_blueprint(bp)
    return app
