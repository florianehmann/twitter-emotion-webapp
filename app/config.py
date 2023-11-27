from dotenv import load_dotenv
import os
# basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
load_dotenv()


class Config:
    GITHUB_URL = os.environ.get('GITHUB_URL') or 'https://github.com/florianehmann/twitter-emotion'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'twitter-emotion-secret'
    INFERENCE_API_TOKEN = os.environ.get('INFERENCE_API_TOKEN') or 'api_token'
    INFERENCE_API_URL = os.environ.get('INFERENCE_API_URL') or 'https://localhost'
