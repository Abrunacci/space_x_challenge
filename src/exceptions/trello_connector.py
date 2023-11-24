"""src.exceptions.trello_connector
All the trello connector exceptions.
"""


class MethodNotAllowed(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TrelloRequestException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
