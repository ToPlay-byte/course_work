from fastapi import FastAPI

from . import models
from .database import Base, engine
from .routers.tasks import router as tasks_router

# Створюємо таблиці автоматично під час старту застосунку (зручно для курсової).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description=(
        "Навчальний REST API для системи управління завданнями.\n\n"
        "Основні можливості:\n"
        "- створення завдання;\n"
        "- перегляд списку завдань (з фільтрацією);\n"
        "- перегляд завдання за ID;\n"
        "- часткове оновлення (PATCH);\n"
        "- видалення завдання."
    ),
    version="1.1.0",
    contact={"name": "Coursework API"},
)

# Підключаємо роутер із CRUD-ендпоінтами для задач.
app.include_router(tasks_router)


@app.get(
    "/",
    tags=["Service"],
    summary="Перевірка доступності API",
    description="Простий службовий ендпоінт для перевірки, що API запущено.",
)
def root() -> dict[str, str]:
    return {"message": "Task Management API is running"}
