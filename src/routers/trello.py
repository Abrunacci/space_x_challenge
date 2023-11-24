"""src.routers.movies
This module contains the endpoints definitions for task router.
"""
from typing import List, Union

from src.schemas.tasks import TaskSchema
from src.services.trello import TrelloService
from fastapi import APIRouter, Response, Request


router = APIRouter()


@router.post("/", tags=["Tasks"], status_code=201)
async def create_task(request: Request, task: TaskSchema) -> str:
    """
    **[POST] /**:

    This endpoint calls the TaskService.create() method.

    **Body**:

    - **task: TaskSchema**
        Task representation.
            ex: {
                "type": "task type",
                "title": "task title",
                "description": "task description" [optional],
                "category": "task category" [optional],
            }

    ***returns: 201**
    """
    service = TrelloService()
    service.create(task.model_dump())
    return "success"
