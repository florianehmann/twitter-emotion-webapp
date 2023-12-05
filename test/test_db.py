"""Test the Functionality of the Base Module of the App"""

import os
import tempfile
import unittest

import sqlalchemy as sa

from app import create_app, db
from app import models
from config import Config


class DBTest(unittest.TestCase):
    """Test the database functionalities of the app"""

    temp_db_file = None
    temp_db_file_name = ''

    @classmethod
    def setUpClass(cls) -> None:
        """Create temporary database file and app"""

        cls.temp_db_file = tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with
        cls.temp_db_file_name = cls.temp_db_file.name + '.db'

        class TestConfig(Config):  # pylint: disable=too-few-public-methods
            """Override Config for this specific TestCase"""
            TESTING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + cls.temp_db_file_name

        app = create_app(TestConfig)
        app_context = app.app_context()
        app_context.push()

    def setUp(self) -> None:
        """Initialize temporary database and populate it with test data"""
        db.create_all()
        self.populate_db()

    def populate_db(self):
        """Populate database with test data"""

        self.user_request = models.UserRequest(tweet_text="tweet text", user_ip="127.0.0.1")
        db.session.add(self.user_request)
        db.session.commit()

    def tearDown(self) -> None:
        """Clear test database"""
        db.drop_all()

    @classmethod
    def tearDownClass(cls) -> None:
        """Delete temporary database file"""
        os.remove(cls.temp_db_file_name)

    def test_reading_user_request(self):
        """Test reading test data back from the database"""
        user_request = db.session.scalar(sa.select(models.UserRequest))
        self.assertEqual(self.user_request.tweet_text, user_request.tweet_text)
        self.assertEqual(self.user_request.user_ip, user_request.user_ip)
