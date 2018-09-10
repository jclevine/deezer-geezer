from unittest.mock import Mock
import json


def build_response_mock(text_response):
    response = Mock()
    response.text = json.dumps(text_response)
    return response
