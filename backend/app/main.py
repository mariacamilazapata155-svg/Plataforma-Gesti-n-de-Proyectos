from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    activity_logs_router,
    attachments_router,
    auth_router,
    boards_router,
    comments_router,
    notifications_router,
    project_members_router,
    projects_router,
    tasks_router,
    users_router,
)
from app.core.config import settings

app = FastAPI(
    title="Work It API",
    description="API REST para la gestión de proyectos Work It.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(boards_router)
app.include_router(tasks_router)
app.include_router(project_members_router)
app.include_router(comments_router)
app.include_router(attachments_router)
app.include_router(activity_logs_router)
app.include_router(notifications_router)


@app.get("/", tags=["Home"])
def root():
    return {"message": "Bienvenido a la API Work It."}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "OK"}
