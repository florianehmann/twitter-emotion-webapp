"""Entrypoint for the Flask Application"""

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app
from app.models import ModelResponse, UserQuery, Tweet
from config import Config


app = create_app(Config)


@app.shell_context_processor
def make_shell_context():
    """Define the Available Identifiers for the `flask shell` Context"""
    return {'sa': sa, 'so': so, 'ModelResponse': ModelResponse, 'UserQuery': UserQuery, 'Tweet': Tweet}
