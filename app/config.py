"""Loads and Contains the Configuration Variables for the Entire App"""

import os

from dotenv import load_dotenv

load_dotenv()


# pylint: disable=too-few-public-methods
class Config:
    """Contains the Configuration Variables for the App"""

    GITHUB_URL = os.environ.get('GITHUB_URL') or "https://github.com/florianehmann/twitter-emotion"
    SECRET_KEY = os.environ.get('SECRET_KEY') or "twitter-emotion-secret"
    INFERENCE_API_TOKEN = os.environ.get('INFERENCE_API_TOKEN') or "api_token"
    INFERENCE_API_URL = (os.environ.get('INFERENCE_API_URL')
                         or "https://api-inference.huggingface.co/models/"
                            "florianehmann/distilbert-base-uncased-finetuned-emotion")
