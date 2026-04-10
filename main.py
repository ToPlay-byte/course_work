from fastapi import FastAPI

import models
from database import Base, engine
from routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="Навчальний REST API для системи управління завданнями",
    version="1.0.0",
)

app.include_router(tasks_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Task Management API is running"}
