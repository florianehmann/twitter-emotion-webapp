"""Main Module of the Webapp"""

from flask import Flask
from flask_bootstrap import Bootstrap
from app.base import bp as base_bp
from app.config import Config

bootstrap = Bootstrap()


def create_app(config_class=Config):
    """Create an instance of the app."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

    app.register_blueprint(base_bp)

    if app.debug or app.testing:
        print('App running in verbose mode')

    return app
