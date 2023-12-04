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
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + temp_db_file + '.db'

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.populate_db()

    def populate_db(self):
        """Populate Database with Test Data"""

        tweet_text = "tweet text"
        model_response_content = {'emotion': 0.43678}

        self.tweet = models.Tweet(text=tweet_text)
        self.user_query = models.UserQuery(tweet=self.tweet, user_ip="127.0.0.1")
        self.model_response = models.ModelResponse(tweet=self.tweet, content=model_response_content)

        db.session.add_all([self.tweet, self.user_query, self.model_response])
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()

    def test_reading_tweet(self):
        """Read a Tweet from the Database and Math the Text"""
        tweet = db.session.scalar(sa.select(models.Tweet))
        self.assertEqual(self.tweet.text, tweet.text)

    def test_user_query_backref(self):
        """Read a UserQuery from the database and see if it has the right Tweet in the tweet field"""
        tweet = db.session.scalar(sa.select(models.Tweet))
        user_query = db.session.scalar(sa.select(models.UserQuery))

        self.assertEqual(tweet.id, user_query.tweet.id)

    def test_model_response_backref(self):
        """Read a ModelResponse from the database and see if it has the right Tweet in the tweet field"""
        tweet = db.session.scalar(sa.select(models.Tweet))
        model_response = db.session.scalar(sa.select(models.ModelResponse))

        self.assertEqual(tweet.id, model_response.tweet.id)

    def test_tweet_backref(self):
        """Read a ModelResponse from the database and see if it has the right Tweet in the tweet field"""
        tweet = db.session.scalar(sa.select(models.Tweet))
        user_query = db.session.scalar(sa.select(models.UserQuery))
        model_response = db.session.scalar(sa.select(models.ModelResponse))

        backref_user_query = db.session.scalar(tweet.user_queries.select())
        self.assertEqual(user_query.id, backref_user_query.id)

        self.assertEqual(model_response.id, tweet.model_response.id)
