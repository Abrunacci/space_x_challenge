"""src.exceptions.trello_service.py
This module contains the custom exceptions for trello_service
"""


class BoardNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
