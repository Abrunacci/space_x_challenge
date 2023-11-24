"""src.services.trello.py
This module contains the TrelloService class representation
"""
import json
import string
from os import environ
from random import randint, choices

from src.connectors.trello_connector import TrelloConnector
from src.exceptions.trello_service import BoardNotFound


class TrelloService:
    """Trello Service class representation."""

    def __init__(self):
        """TrelloService class initialization."""
        self.board_id = None
        self.board_labels = None
        self.board_lists = None
        self.board_users = None
        self._get_board_info()

        self.create_by_type = {
            "task": self._create_task,
            "issue": self._create_issue,
            "bug": self._create_bug,
        }

    def create(self, data: dict) -> None:
        """
        Create method to get call from router
        :param data:
            Task dict representation
        :return:
        """
        self.create_by_type[data.get('type')](data)

    def _get_board_info(self):
        """_get_board_id
        This function calls TrelloConnector and fills self.board_id.
        """
        user = environ.get("TRELLO_API_USER")
        admin_user_boards = TrelloConnector.execute_request(
            "GET", endpoint=f"members/{user}"
        )
        for board_id in admin_user_boards.get("idBoards"):
            board_data = TrelloConnector.execute_request(
                "GET",
                endpoint=f"boards/{board_id}",
                params={
                    "member_fields": "id,username",
                    "members": "all",
                    "lists": "all",
                    "list_fields": "id,name",
                    "labels": "all",
                    "label_fields": "id,name",
                },
            )
            if board_data.get("name") == environ.get("BOARD_NAME"):
                self.board_id = board_data.get("id")
                self.board_labels = board_data.get("labels")
                self.board_users = board_data.get("members")
                self.board_lists = board_data.get("lists")
                break
        else:
            raise BoardNotFound(f"Can't find the board:{environ.get('BOARD_NAME')}")

    def _create(self, card_info: dict, list_name: str) -> dict:
        """
        This function calls the TrelloConnector to create a new card
        :param card_info:
            card data dict representation.
        :param list_name:
            The column name where all the tasks will be created
        :return:
        """
        endpoint = "cards"
        params = {}
        for lst in self.board_lists:
            if lst.get("name") == list_name:
                params["idList"] = lst.get("id")
                card_info["idList"] = lst.get("id")
        return TrelloConnector.execute_request(
            "POST", endpoint=endpoint, body=card_info, params=params
        )

    def _create_issue(self, task: dict) -> None:
        """
        Create a card which type is issue
        :param task:
            Task dict representation
        :return:
        """
        card_info = {
            "name": task.get("title"),
            "desc": task.get("description"),
        }
        self._create(card_info, "To Do")

    def _create_task(self, task: dict) -> None:
        """
        Create a card which type is task
        :param task:
            Task dict representation
        :return:
        """
        card_info = {
            "name": task.get("title"),
        }
        created_card = self._create(card_info, "To Do")
        self._set_label(task.get("category"), created_card)

    def _create_bug(self, task: dict) -> None:
        """
        Create a card which type is bug
        :param task:
            Task dict representation
        :return:
        """
        number = randint(1000, 10000)
        word = "".join(choices(string.ascii_lowercase, k=4))
        card_info = {"name": f"bug-{word}-{number}", "desc": task.get("description")}
        created_card = self._create(card_info, "To Do")
        self._set_label("bug", created_card)
        self._set_member(created_card)

    def _set_label(self, category: str, card: dict) -> None:
        """
        Set label to a card
        :param category:
            category string representation
        :param card:
            card dict representation
        :return:
        """
        query_params = {}
        for label in self.board_labels:
            if label.get("name").lower() == category.lower():
                query_params["value"] = label.get("id")
        endpoint = f"cards/{card.get('id')}/idLabels"
        TrelloConnector.execute_request("POST", endpoint=endpoint, params=query_params)

    def _set_member(self, card: dict) -> None:
        """
        Set member to a card.
        For now, this function will only receive the card and assign a random member from the board
        :param card:
            card dict representation
        :return:
        """
        endpoint = f"cards/{card.get('id')}/idMembers"
        selection = choices(self.board_users)[0].get("id")
        query_params = {"value": selection}
        TrelloConnector.execute_request("POST", endpoint=endpoint, params=query_params)
