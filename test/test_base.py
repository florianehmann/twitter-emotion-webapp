"""Test the Functionality of the Base Module of the App"""

import unittest

from app import create_app


# pylint: disable=too-few-public-methods
class TestConfig:
    """Override Config for Testing Purposes"""
    TESTING = True
    SECRET_KEY = 'test-key'


class BaseTest(unittest.TestCase):
    """Test the Most Basic Functionalities of the App"""

    # pylint: disable=missing-function-docstring
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_testing_mode(self):
        self.assertEqual(True, self.app.config['TESTING'])

    def test_index_reachable(self):
        client = self.app.test_client()
        self.assertEqual(200, client.get('/').status_code)
