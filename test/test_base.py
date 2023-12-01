"""Test the Functionality of the Base Module of the App"""

import unittest

from app import create_app
from config import Config


Config.TESTING = True


class BaseTest(unittest.TestCase):
    """Test the Most Basic Functionalities of the App"""

    # pylint: disable=missing-function-docstring
    def setUp(self) -> None:
        self.app = create_app(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_testing_mode(self):
        self.assertEqual(True, self.app.config['TESTING'])

    def test_index_reachable(self):
        client = self.app.test_client()
        self.assertEqual(200, client.get('/').status_code)
