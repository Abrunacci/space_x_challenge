from src.schemas.tasks import TaskSchema


def test_task_schema():
    assert TaskSchema(type="bug", description="Otro bug").model_dump() ==  {'category': None, 'description': 'Otro bug', 'title': None, 'type': 'bug'}
