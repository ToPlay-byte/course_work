from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..enums import TaskPriority, TaskStatus

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Завдання не знайдено"}},
)


@router.post(
    "",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити завдання",
    description="Створює нове завдання та повертає його у відповіді.",
)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)) -> schemas.TaskResponse:
    return crud.create_task(db, task)


@router.get(
    "",
    response_model=list[schemas.TaskResponse],
    summary="Отримати список завдань",
    description="Повертає список завдань. За потреби можна фільтрувати за status і priority.",
)
def read_tasks(
    status: TaskStatus | None = Query(default=None, description="Фільтр за статусом"),
    priority: TaskPriority | None = Query(default=None, description="Фільтр за пріоритетом"),
    db: Session = Depends(get_db),
) -> list[schemas.TaskResponse]:
    return crud.get_tasks(db, status=status, priority=priority)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Отримати завдання за ID",
    description="Повертає одне завдання за його ідентифікатором.",
)
def read_task(task_id: int, db: Session = Depends(get_db)) -> schemas.TaskResponse:
    db_task = crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Оновити завдання",
    description="Частково оновлює поля завдання за ID.",
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
) -> schemas.TaskResponse:
    db_task = crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Видалити завдання",
    description="Видаляє завдання за ID. У разі успіху повертає 204 No Content.",
)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> Response:
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
