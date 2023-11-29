"""Functionality for the Emotion Inference Using the Classification Model"""

from typing import Union, List

import requests

from app.config import Config


headers = {"Authorization": f"Bearer {Config.INFERENCE_API_TOKEN}"}
LABEL_NAMES = {
    'LABEL_0': 'sadness',
    'LABEL_1': 'joy',
    'LABEL_2': 'love',
    'LABEL_3': 'anger',
    'LABEL_4': 'fear',
    'LABEL_5': 'surprise',
}


class ModelQueryException(Exception):
    """Exception for Unspecified Problems while Querying the Model"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ModelLoadingException(Exception):
    """Exception to Raise When the Model is Not Loaded Yet"""


def query_model(tweet: str) -> [List[dict]]:
    """Sends an API Request to the Hosted Model and Returns the Result in Usable Form"""

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

    # replace model labels with human-readable names
    for classification in classifications:
        classification['label'] = LABEL_NAMES[classification['label']]

    return classifications
