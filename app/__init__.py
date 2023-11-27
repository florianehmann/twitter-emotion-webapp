from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_class=Config):
    """Create an instance of the app."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

    from app.base import bp as base_bp
    app.register_blueprint(base_bp)

    if app.debug or app.testing:
        print('App running in verbose mode')

    return app
