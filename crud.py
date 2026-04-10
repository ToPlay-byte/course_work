from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .enums import TaskPriority, TaskStatus


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Створює нове завдання в БД."""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(
    db: Session,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[models.Task]:
    """Повертає список завдань з необов'язковими фільтрами за статусом і пріоритетом."""
    stmt = select(models.Task)

    if status is not None:
        stmt = stmt.where(models.Task.status == status)
    if priority is not None:
        stmt = stmt.where(models.Task.priority == priority)

    stmt = stmt.order_by(models.Task.created_at.desc())
    return list(db.scalars(stmt).all())


def get_task(db: Session, task_id: int) -> models.Task | None:
    """Повертає одне завдання за ID або None, якщо не знайдено."""
    stmt = select(models.Task).where(models.Task.id == task_id)
    return db.scalars(stmt).first()


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> models.Task | None:
    """Оновлює поля завдання за ID (часткове оновлення)."""
    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Видаляє завдання за ID. Повертає True, якщо видалено."""
    db_task = get_task(db, task_id)
    if db_task is None:
        return False

    db.delete(db_task)
    db.commit()
    return True
