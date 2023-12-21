"""Functionality for the Emotion Inference Using the Classification Model"""

from typing import Union, List

import requests

from config import Config


headers = {"Authorization": f"Bearer {Config.INFERENCE_API_TOKEN}"}


class ModelQueryException(Exception):
    """Exception for Unspecified Problems while Querying the Model"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ModelLoadingException(Exception):
    """Exception to Raise When the Model is Not Loaded Yet"""


def query_model(tweet: str) -> [List[dict]]:
    """Sends an API request to the hosted model and returns the result in usable form"""

    try:
        response: Union[dict, List[List[dict]]] = requests.post(Config.INFERENCE_API_URL, headers=headers,
                                                                json={'inputs': tweet}, timeout=5).json()
    except requests.exceptions.ConnectionError as e:
        raise ModelQueryException("Can't connect to the model at the moment 🤔") from e

    # got an error from HuggingFace
    if isinstance(response, dict):
        if "currently loading" in response['error']:
            raise ModelLoadingException()
        raise ModelQueryException(response['error'])

    classifications = response[0]

    # sort classifications by score in descending order
    classifications = sorted(classifications, key=lambda c: c['score'], reverse=True)

    return classifications
