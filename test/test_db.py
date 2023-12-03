"""Test the Functionality of the Base Module of the App"""

import tempfile
import unittest

import sqlalchemy as sa

from app import create_app, db
from app import models
from config import Config


class DBTest(unittest.TestCase):
    """Test the Database Functionalities of the App"""

    def setUp(self) -> None:
        """Creates a Temporary Database and Initializes the App"""
        temp_db_file = tempfile.NamedTemporaryFile().name  # pylint: disable=consider-using-with

        class TestConfig(Config):  # pylint: disable=too-few-public-methods
            """Override Config for this Specific TestCase"""
            TESTING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + temp_db_file

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.populate_db()

    def populate_db(self):
        """Populate Database with Test Data"""

        self.tweet_text = "tweet text"
        self.model_response_content = {'emotion': 0.43678}

        tweet = models.Tweet(text=self.tweet_text)
        user_query = models.UserQuery(tweet=tweet, user_ip="127.0.0.1")
        model_response = models.ModelResponse(tweet=tweet, content=self.model_response_content)

        db.session.add_all([tweet, user_query, model_response])
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()

    def test_reading_tweet(self):
        """Read a Tweet from the Database and Math the Text"""
        tweet = db.session.scalar(sa.select(models.Tweet))
        self.assertEqual(self.tweet_text, tweet.text)
