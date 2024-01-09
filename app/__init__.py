"""Main Module of the Webapp"""

import logging
import os.path
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()


# pylint: disable=import-outside-toplevel
def create_app(config_class=Config):
    """Create an Instance of the App"""

    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprint imports inside the factory to prevent cyclic imports

    from app.base import bp as base_bp
    app.register_blueprint(base_bp)

    set_up_logging(app)

    app.logger.info("App started")
    app.logger.debug("App running in verbose mode")

    return app


def set_up_logging(app):
    """Set Up Logging for the Application and Model Queries"""

    if not app.config['LOG_TO_STDOUT'] and not os.path.exists('logs'):
        os.mkdir('logs')

    # application logging

    log_level = logging.DEBUG if app.debug or app.testing else logging.INFO
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        app.logger.addHandler(stream_handler)
    else:
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=10)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s"))
        app.logger.addHandler(file_handler)

    app.logger.setLevel(log_level)

    # query logging

    app.query_logger = logging.Logger('QueryLogger')
    app.query_logger.setLevel(logging.INFO)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        app.query_logger.addHandler(stream_handler)
    else:
        file_handler = RotatingFileHandler('logs/queries.log', maxBytes=10000, backupCount=10)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s QUERY]: %(message)s"))
        app.query_logger.addHandler(file_handler)


from app import models  # pylint: disable=wrong-import-position,ungrouped-imports
