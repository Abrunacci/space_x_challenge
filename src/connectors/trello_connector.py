"""src.connectors.trello_connector.py
This module contains the Trello connector class representation.
"""
from os import environ

import httpx

from src.exceptions.trello_connector import MethodNotAllowed, TrelloRequestException


class TrelloConnector:
    """Trello connector class representation."""

    API_TOKEN = environ.get("TRELLO_API_TOKEN")
    API_KEY = environ.get("TRELLO_API_KEY")
    USER = environ.get("TRELLO_API_USER")
    API_BASE_URL = environ.get("TRELLO_API_BASE_URL")
    METHOD_MAPPER = {"GET": httpx.get, "POST": httpx.post}

    @classmethod
    def execute_request(
        cls, method: str, endpoint: str, params: dict = None, body: dict = None
    ) -> dict:
        """
        This method performs the API request calls
        :param method:
            HTTP method string representation (Uppercase).
            Ex: "POST"
        :param endpoint:
            The Trello API endpoint string representation
        :param params:
            Additional query_params dict representation
        :param body:
            POST body content
        :return: dictionary representation of response
        """
        request_content = {
            "params": {
                "key": cls.API_KEY,
                "token": cls.API_TOKEN,
            },
            "url": f"{cls.API_BASE_URL}{endpoint}",
        }

        if method not in cls.METHOD_MAPPER:
            raise MethodNotAllowed(f"Method {method} not allowed")

        if body:
            request_content["json"] = body
        if params:
            request_content["params"].update(params)
        response = cls.METHOD_MAPPER[method](**request_content)
        if response.status_code != 200:
            raise TrelloRequestException(f"Trello request status_code: {response.status_code}")
        return response.json()
