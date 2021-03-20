import os

basedir = os.path.abspath(os.path.dirname(__file__))

# database access
# DB_HOST = 'miloszhoc.cloud'
# DB_USER = 'postgres'
# DB_PASS = 'cloud_app!'
# DB_NAME = 'cloud_app_db'
# DB_TABLE = 'url'
# DB_PORT = 5433

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_TABLE = os.environ.get('DB_TABLE')
DB_PORT = os.environ.get('DB_PORT')


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/dev-app.db".format(basedir)


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/test-app.db".format(basedir)


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DB_URI = 'postgresql+psycopg2://{user}:{passwd}@{url}:{port}/{db}'.format(user=DB_USER,
                                                                              passwd=DB_PASS,
                                                                              url=DB_HOST,
                                                                              port=DB_PORT,
                                                                              db=DB_NAME)


# email data
SENDGRID_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL')

EXPORT_CFGS = [TestingConfig, DevelopmentConfig, ProductionConfig]
config_names = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CFGS}
