"""
Init flask-books app
SQLAlchemy config
"""
import logging
from logging import FileHandler, Formatter
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


from config import app_config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    """Flask application factory"""
    _app = Flask(__name__)
    _app.config.from_object(app_config[config_name])
    db.init_app(_app)
    ma.init_app(_app)
    migrate.init_app(_app, db)

    return _app


app = create_app('test')
api = Api(app=app)


file_handler = FileHandler('error.log')
file_handler.setFormatter(
    Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
)
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
