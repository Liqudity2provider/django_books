import os
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Configuration"""

    SECRET_KEY = "457f8208-6e3c-4f60-9adb-944fa6edc08b"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:alex2811@localhost:5432/flask-books'


class DevelopmentConfig(Config):
    """Development config"""

    DEBUG = True


class ProductionConfig(Config):
    """Production config"""

    DEBUG = False
    TESTING = False


class TestConfig(Config):
    """Testing config"""

    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///new_db.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
