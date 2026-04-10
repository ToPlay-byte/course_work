from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Схема створення нового завдання."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Коротка назва завдання (обов'язкове поле).",
        examples=["Підготувати розділ курсової"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Детальний опис завдання (необов'язково).",
        examples=["Описати архітектуру REST API та моделі даних."],
    )
    status: TaskStatus = Field(
        default=TaskStatus.NEW,
        description="Поточний статус завдання: new, in_progress або done.",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Пріоритет завдання: low, medium або high.",
    )

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        """Обрізає пробіли і забороняє порожній title."""
        value = value.strip()
        if not value:
            raise ValueError("title must not be empty")
        return value


class TaskUpdate(BaseModel):
    """Схема часткового оновлення завдання (PATCH)."""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Нова назва завдання.",
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Новий опис завдання.",
    )
    status: TaskStatus | None = Field(
        default=None,
        description="Новий статус завдання.",
    )
    priority: TaskPriority | None = Field(
        default=None,
        description="Новий пріоритет завдання.",
    )

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str | None) -> str | None:
        """Обрізає пробіли і не дозволяє передати порожню назву."""
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("title must not be empty")
        return value


class TaskResponse(BaseModel):
    """Схема відповіді з даними завдання."""

    id: int = Field(description="Унікальний ідентифікатор завдання.")
    title: str = Field(description="Назва завдання.")
    description: str | None = Field(default=None, description="Опис завдання.")
    status: TaskStatus = Field(description="Статус завдання.")
    priority: TaskPriority = Field(description="Пріоритет завдання.")
    created_at: datetime = Field(description="Дата і час створення (UTC).")

    model_config = ConfigDict(from_attributes=True)
