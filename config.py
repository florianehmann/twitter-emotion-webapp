"""Loads and Contains the Configuration Variables for the Entire App"""

import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


# pylint: disable=too-few-public-methods
class Config:
    """Contains the Configuration Variables for the App"""

    GITHUB_URL = os.environ.get('GITHUB_URL') or "https://github.com/florianehmann/twitter-emotion-webapp"
    SECRET_KEY = os.environ.get('SECRET_KEY') or "twitter-emotion-secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///" + os.path.join(basedir, 'app.db')
    INFERENCE_API_TOKEN = os.environ.get('INFERENCE_API_TOKEN') or "api_token"
    INFERENCE_API_URL = (os.environ.get('INFERENCE_API_URL')
                         or "https://api-inference.huggingface.co/models/"
                            "florianehmann/xlm-roberta-base-finetuned-emotion")
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LINKEDIN_URL = os.environ.get('LINKEDIN_URL') or ""
