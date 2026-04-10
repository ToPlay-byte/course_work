from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = TaskStatus.NEW
    priority: TaskPriority = TaskPriority.MEDIUM

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be empty")
        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("title must not be empty")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
