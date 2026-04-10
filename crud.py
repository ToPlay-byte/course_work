from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session) -> list[models.Task]:
    stmt = select(models.Task).order_by(models.Task.created_at.desc())
    return list(db.scalars(stmt).all())


def get_task(db: Session, task_id: int) -> models.Task | None:
    stmt = select(models.Task).where(models.Task.id == task_id)
    return db.scalars(stmt).first()


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> models.Task | None:
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True
