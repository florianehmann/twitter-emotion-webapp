"""Test functionalities of the `app.inference` module"""

import unittest
from unittest.mock import create_autospec, Mock, patch

import requests

from app.inference import ModelLoadingException, ModelQueryException, query_model


class SuccessfulResponseMock:  # pylint: disable=too-few-public-methods
    """Mocks the response to a successful API call"""
    @staticmethod
    def json():  # pylint: disable=missing-function-docstring
        return [[
            {'label': 'anger', 'score': 0.5847911834716797},
            {'label': 'fear', 'score': 0.19749358296394348},
            {'label': 'joy', 'score': 0.08343658596277237},
            {'label': 'sadness', 'score': 0.08297344297170639},
            {'label': 'surprise', 'score': 0.03506644442677498},
            {'label': 'love', 'score': 0.016238784417510033}
        ]]


class ModelLoadingResponseMock:  # pylint: disable=too-few-public-methods
    """Mocks the "model loading" response to an API call"""

    content = {
        'error': 'Model ... is currently loading',
        'estimated_time': 44.48772048950195
    }

    @classmethod
    def json(cls):  # pylint: disable=missing-function-docstring
        return cls.content


class InferenceTest(unittest.TestCase):
    """Test functionalities of the `app.inference` module"""

    @patch("requests.post", new=Mock(return_value='mocked'))
    def test_patching(self):
        """Test if `requests.post` is patched successfully"""
        self.assertEqual(requests.post(url="", timeout=1), "mocked")

    @patch("requests.post", new=create_autospec(requests.post, side_effect=requests.exceptions.ConnectionError))
    def test_connection_error(self):
        """Test if a ModelQueryException is raised Successfully"""
        with self.assertRaisesRegex(ModelQueryException, "connect to the model at the moment"):
            query_model("test tweet")

    @patch("requests.post", new=create_autospec(requests.post, return_value=ModelLoadingResponseMock()))
    def test_model_loading(self):
        """Test if a ModelLoadingException is raised"""

        with self.assertRaises(ModelLoadingException) as cm:
            query_model("test tweet")

        self.assertAlmostEqual(ModelLoadingResponseMock.content['estimated_time'], cm.exception.time_estimate)

    @patch("requests.post", new=create_autospec(requests.post, return_value=SuccessfulResponseMock()))
    def test_successful_response(self):
        """Test the behavior under a successful response from the external API"""

        classifications = query_model("test tweet")

        self.assertTrue(len(classifications) > 0)
        self.assertIn('label', classifications[0])
        self.assertIn('score', classifications[0])
