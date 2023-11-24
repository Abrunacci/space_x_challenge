"""tests.test_trello_service.py
This module contains the test for TrelloService class representation.
"""
from unittest.mock import patch, call

import pytest

from src.exceptions.trello_service import BoardNotFound
from src.services.trello import TrelloService


@patch("src.services.trello.TrelloConnector")
def test_trello_service_instantiation(
    fake_connector, fake_responses_from_trello
):
    """This function tests the TrelloService instantiation method.
    TrelloService should be all the correct values once initialized.
    """
    fake_connector.execute_request.side_effect = [
        fake_responses_from_trello.get("memberInfo"),
        fake_responses_from_trello.get("boardInfo"),
    ]
    trello_service = TrelloService()
    board_data = fake_responses_from_trello.get("boardInfo")
    assert trello_service.board_id == board_data.get("id")
    assert trello_service.board_users == board_data.get("members")
    assert trello_service.board_labels == board_data.get("labels")
    assert trello_service.board_lists == board_data.get("lists")


@patch("src.services.trello.TrelloConnector")
def test_trello_service_instantiation_board_not_found(
    fake_connector, fake_responses_from_trello
):
    """This function tests the TrelloService instantiation method.
    TrelloService should be all the correct values once initialized.
    """
    fake_connector.execute_request.side_effect = [
        fake_responses_from_trello.get("memberInfo"),
        {},
    ]
    with pytest.raises(BoardNotFound):
        TrelloService()


@patch("src.services.trello.TrelloConnector")
def test_trello_service_create_issue(fake_connector, fake_responses_from_trello):
    """This function tests the TrelloService create_issue method.
    Verifies all calls made in the card creation process for "issue"
    """
    fake_connector.execute_request.side_effect = [
        fake_responses_from_trello.get("memberInfo"),
        fake_responses_from_trello.get("boardInfo"),
        fake_responses_from_trello.get("cardCreation"),
    ]
    card = {"type": "issue", "title": "New Task", "description": "Some description!"}
    service = TrelloService()
    service.create_by_type[card.get("type")](card)
    assert fake_connector.execute_request.call_args_list == [
        call("GET", endpoint="members/abrunacci87userintegration1"),
        call(
            "GET",
            endpoint="boards/1234",
            params={
                "member_fields": "id,username",
                "members": "all",
                "lists": "all",
                "list_fields": "id,name",
                "labels": "all",
                "label_fields": "id,name",
            },
        ),
        call(
            "POST",
            endpoint="cards",
            body={"name": "New Task", "desc": "Some description!", "idList": "ABC123"},
            params={"idList": "ABC123"},
        ),
    ]


@patch("src.services.trello.TrelloConnector")
def test_trello_service_create_task(fake_connector, fake_responses_from_trello):
    """This function tests the TrelloService _create_task method.
        Verifies all calls made in the card creation process for "task"
    """
    fake_connector.execute_request.side_effect = [
        fake_responses_from_trello.get("memberInfo"),
        fake_responses_from_trello.get("boardInfo"),
        fake_responses_from_trello.get("cardCreation"),
        fake_responses_from_trello.get("labelUpdate"),
    ]
    card = {"type": "task", "title": "New Task created", "category": "Test"}
    service = TrelloService()
    service.create_by_type[card.get("type")](card)
    assert fake_connector.execute_request.call_args_list == [
        call("GET", endpoint="members/abrunacci87userintegration1"),
        call(
            "GET",
            endpoint="boards/1234",
            params={
                "member_fields": "id,username",
                "members": "all",
                "lists": "all",
                "list_fields": "id,name",
                "labels": "all",
                "label_fields": "id,name",
            },
        ),
        call(
            "POST",
            endpoint="cards",
            body={"name": "New Task created", "idList": "ABC123"},
            params={"idList": "ABC123"},
        ),
        call(
            "POST",
            endpoint="cards/656011bbdd1f4ea45e5735c8/idLabels",
            params={"value": "655f57b2b8cf520e8bbf26cc"},
        ),
    ]


@patch("src.services.trello.TrelloConnector")
@patch("src.services.trello.randint")
@patch("src.services.trello.choices")
def test_trello_service_create_bug(
    fake_choices, fake_randint, fake_connector, fake_responses_from_trello
):
    """This function tests the TrelloService _create_bug method.
        Verifies all calls made in the card creation process for "bug"
    """
    fake_randint.return_value = 1234
    fake_choices.side_effect = ["abcd", [{"id": "userId"}]]
    fake_connector.execute_request.side_effect = [
        fake_responses_from_trello.get("memberInfo"),
        fake_responses_from_trello.get("boardInfo"),
        fake_responses_from_trello.get("cardCreation"),
        fake_responses_from_trello.get("labelUpdate"),
        fake_responses_from_trello.get("memberUpdate"),
    ]
    card = {"type": "bug", "description": "Some description!"}
    service = TrelloService()
    service.create_by_type[card.get("type")](card)
    assert fake_connector.execute_request.call_args_list == [
        call("GET", endpoint="members/abrunacci87userintegration1"),
        call(
            "GET",
            endpoint="boards/1234",
            params={
                "member_fields": "id,username",
                "members": "all",
                "lists": "all",
                "list_fields": "id,name",
                "labels": "all",
                "label_fields": "id,name",
            },
        ),
        call(
            "POST",
            endpoint="cards",
            body={
                "name": "bug-abcd-1234",
                "desc": "Some description!",
                "idList": "ABC123",
            },
            params={"idList": "ABC123"},
        ),
        call(
            "POST",
            endpoint="cards/656011bbdd1f4ea45e5735c8/idLabels",
            params={"value": "655f57b2b8cf520e8bbf26c6"},
        ),
        call(
            "POST",
            endpoint="cards/656011bbdd1f4ea45e5735c8/idMembers",
            params={"value": "userId"},
        ),
    ]