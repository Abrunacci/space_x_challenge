from enum import Enum

from typing import Optional
from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    type: str
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

