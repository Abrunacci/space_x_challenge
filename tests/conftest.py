import pytest


@pytest.fixture()
def fake_responses_from_trello():
    return {
        "memberInfo": {"id": "ABC1", "idBoards": ["1234"]},
        "boardInfo": {
            "name": "SpaceXChallenge",
            "members": [{"id": "ABC1", "username": "UserName"}],
            "lists": [{"id": "ABC123", "name": "To Do"}],
            "id": "1234",
            "labels": [
                {"id": "655f57b2b8cf520e8bbf26cc", "name": "Test"},
                {"id": "655f9b4e01cc65d8ae94c973", "name": "Research"},
                {"id": "655f57b2b8cf520e8bbf26c6", "name": "Bug"},
                {"id": "655f57b2b8cf520e8bbf26bd", "name": "Maintenance"},
            ],
        },
        "cardCreation": {"id": "656011bbdd1f4ea45e5735c8"},
        "labelUpdate": ["labelId1"],
        "memberUpdate": [{"id": "user_id"}],
    }
