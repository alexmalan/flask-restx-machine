"""Flask configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.dirname(path.abspath(__file__))
ENV = environ.get("FLASK_ENV", "default")


if ENV == "development":
    dotenv_file = ".env.development"
else:
    dotenv_file = ".env"

load_dotenv(path.join(basedir, dotenv_file))


class Config:
    """Configuration class."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_OAUTH_REALM = "-"
    SWAGGER_UI_OAUTH_APP_NAME = "Flask Rest Vending Machine API"
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{environ.get('DATABASE_USERNAME')}:{environ.get('DATABASE_PASSWORD')}@"
        f"{environ.get('DATABASE_HOST')}:{environ.get('DATABASE_PORT')}/{environ.get('DATABASE_NAME')}"
    )
    SECRET_KEY = environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    """Development configuration class."""

    SECRET_KEY = environ.get("SECRET_KEY")


class TestConfig(Config):
    """Testing configuration class."""

    TESTING = True
    SECRET_KEY = environ.get("SECRET_KEY")

    # For test purpose use a new database
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{environ.get('DATABASE_USERNAME')}:{environ.get('DATABASE_PASSWORD')}@"
        f"{environ.get('DATABASE_HOST')}:{environ.get('DATABASE_PORT')}/{environ.get('TEST_DATABASE_NAME')}"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config_by_name = dict(
    development=DevelopmentConfig, default=DevelopmentConfig, testing=TestConfig
)
