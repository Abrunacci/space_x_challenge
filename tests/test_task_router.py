from unittest.mock import patch

from fastapi.testclient import TestClient

import src.routers.trello
from src.main import app

client = TestClient(app)


def test_task_creation():
    """testing task creation"""
    response = client.post('/', json={"type": "bug", "description": "yey!"})
    assert response.status_code == 201
