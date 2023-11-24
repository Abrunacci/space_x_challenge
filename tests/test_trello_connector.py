"""tests.test_trello_connector.py
This module contains all the trello connector tests
"""
from os import environ

from unittest.mock import patch, MagicMock

import httpx
import pytest

from src.connectors.trello_connector import TrelloConnector
from src.exceptions.trello_connector import MethodNotAllowed, TrelloRequestException
from tests.mocks.mocked_response import MockedResponse


def test_trello_connector_properties():
    """Test trello connector properties
    This test checks that all the TrelloConnector class representation attributes
    has the same value as their env var equivalent"""
    assert TrelloConnector.API_KEY == environ.get("TRELLO_API_KEY")
    assert TrelloConnector.API_TOKEN == environ.get("TRELLO_API_TOKEN")
    assert TrelloConnector.USER == environ.get("TRELLO_API_USER")
    assert TrelloConnector.API_BASE_URL == environ.get("TRELLO_API_BASE_URL")
    assert TrelloConnector.METHOD_MAPPER == {"GET":httpx.get, "POST": httpx.post}


def test_trello_connector_execute_get_request():
    """Test trello connector request execution.
    This test checks that the httpx library performs a call with the correct query params, url and method
    """
    with patch("src.connectors.trello_connector.httpx") as client:
        client.get = MagicMock(return_value=MockedResponse(status_code=200))
        TrelloConnector.METHOD_MAPPER["GET"] = client.get
        query_params = {
            "key": environ.get("TRELLO_API_KEY"),
            "token": environ.get("TRELLO_API_TOKEN"),
        }
        base_url = environ.get("TRELLO_API_BASE_URL")
        endpoint = "members/member1"
        url = f"{base_url}{endpoint}"

        response = TrelloConnector.execute_request(method="GET", endpoint=endpoint)
        client.get.assert_called_once_with(url=url, params=query_params)
        assert response == {}


def test_trello_connector_execute_raise_method_not_allowed():
    """Test trello connector request execution.
    This test checks that the httpx library performs a call with the correct query params, url and method
    """
    with pytest.raises(MethodNotAllowed):
        TrelloConnector.execute_request(method="PATCH", endpoint="endpoint")


def test_trello_connector_execute_raise_trello_request_exception():
    """Test trello connector request execution.
    This test checks that the httpx library performs a call with the correct query params, url and method
    """
    with patch("src.connectors.trello_connector.httpx") as fake_client:
        fake_client.get = MagicMock(return_value=MockedResponse(status_code=404))
        TrelloConnector.METHOD_MAPPER["GET"] = fake_client.get
        with pytest.raises(TrelloRequestException):
            response = TrelloConnector.execute_request(method="GET", endpoint="endpoint")




def test_trello_connector_execute_post_request():
    """Test trello connector request execution.
    This test checks that the httpx library performs a call with the correct query params, url and method
    """
    with patch("src.connectors.trello_connector.httpx") as client:
        client.post = MagicMock(return_value=MockedResponse(status_code=200))
        TrelloConnector.METHOD_MAPPER["POST"] = client.post
        query_params = {
            "key": environ.get("TRELLO_API_KEY"),
            "token": environ.get("TRELLO_API_TOKEN"),
        }
        body = {"field": "field"}
        base_url = environ.get("TRELLO_API_BASE_URL")
        endpoint = ""
        url = f"{base_url}{endpoint}"

        response = TrelloConnector.execute_request(
            method="POST", endpoint=endpoint, body=body
        )
        client.post.assert_called_once_with(url=url, params=query_params, json=body)
        assert response == {}


def test_trello_connector_execute_post_request_with_additional_params():
    """Test trello connector request execution.
    This test checks that the httpx library performs a call with the correct query params, url and method
    """
    with patch("src.connectors.trello_connector.httpx") as client:
        client.post = MagicMock(return_value=MockedResponse(status_code=200))
        TrelloConnector.METHOD_MAPPER["POST"] = client.post
        query_params = {
            "key": environ.get("TRELLO_API_KEY"),
            "token": environ.get("TRELLO_API_TOKEN"),
            "value": "1234"
        }
        body = {"field": "field"}
        base_url = environ.get("TRELLO_API_BASE_URL")
        endpoint = ""
        url = f"{base_url}{endpoint}"

        response = TrelloConnector.execute_request(
            method="POST", endpoint=endpoint, body=body, params={"value": "1234"}
        )
        client.post.assert_called_once_with(url=url, params=query_params, json=body)
        assert response == {}
