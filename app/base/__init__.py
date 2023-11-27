"""Most Fundamental Components of the App"""

from flask import Blueprint

bp = Blueprint('base', __name__)

from app.base import routes
