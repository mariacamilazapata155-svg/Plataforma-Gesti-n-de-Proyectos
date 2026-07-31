import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.db.base_imports as _  # noqa: F401
from app.core.security import create_access_token, hash_password
from app.db.base import Base
from app.db.session import get_db
from app.enums.activity_action import ActivityAction
from app.enums.notification_type import NotificationType
from app.enums.project_role import ProjectRole
from app.main import app
from app.models.activity_log import ActivityLog
from app.models.attachment import Attachment
from app.models.board import Board
from app.models.comment import Comment
from app.models.notification import Notification
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.user import User

# --------------------------------------------------
# DATABASE
# --------------------------------------------------


@pytest.fixture()
def db_session():

    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# --------------------------------------------------
# CLIENT
# --------------------------------------------------


@pytest.fixture()
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# --------------------------------------------------
# USERS
# --------------------------------------------------


@pytest.fixture()
def users(db_session):

    created_users = {
        "owner": User(
            username="owner",
            email="owner@example.com",
            hashed_password=hash_password("password"),
        ),
        "member": User(
            username="member",
            email="member@example.com",
            hashed_password=hash_password("password"),
        ),
        "viewer": User(
            username="viewer",
            email="viewer@example.com",
            hashed_password=hash_password("password"),
        ),
        "other_member": User(
            username="other_member",
            email="other_member@example.com",
            hashed_password=hash_password("password"),
        ),
        "outsider": User(
            username="outsider",
            email="outsider@example.com",
            hashed_password=hash_password("password"),
        ),
    }

    db_session.add_all(created_users.values())
    db_session.commit()

    for user in created_users.values():
        db_session.refresh(user)

    return created_users


# --------------------------------------------------
# AUTH HEADERS
# --------------------------------------------------


def auth_headers(user: User):

    token = create_access_token(user.id)

    return {
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture()
def owner_headers(users):
    return auth_headers(users["owner"])


@pytest.fixture()
def member_headers(users):
    return auth_headers(users["member"])


@pytest.fixture()
def viewer_headers(users):
    return auth_headers(users["viewer"])


@pytest.fixture()
def outsider_headers(users):
    return auth_headers(users["outsider"])


@pytest.fixture()
def anonymous_headers():
    return {}


# --------------------------------------------------
# AUTHORIZATION DATA
# --------------------------------------------------


@pytest.fixture()
def authorization_data(
    db_session,
    users,
):

    # ----------------------------
    # Projects
    # ----------------------------

    project = Project(
        title="Proyecto compartido",
        owner_id=users["owner"].id,
    )

    private_project = Project(
        title="Proyecto privado",
        owner_id=users["outsider"].id,
    )

    db_session.add_all(
        [
            project,
            private_project,
        ]
    )

    db_session.flush()

    # ----------------------------
    # Members
    # ----------------------------

    owner_membership = ProjectMember(
        project_id=project.id,
        user_id=users["owner"].id,
        role=ProjectRole.OWNER,
    )

    member_membership = ProjectMember(
        project_id=project.id,
        user_id=users["member"].id,
        role=ProjectRole.MEMBER,
    )

    viewer_membership = ProjectMember(
        project_id=project.id,
        user_id=users["viewer"].id,
        role=ProjectRole.VIEWER,
    )

    other_member_membership = ProjectMember(
        project_id=project.id,
        user_id=users["other_member"].id,
        role=ProjectRole.MEMBER,
    )

    outsider_membership = ProjectMember(
        project_id=private_project.id,
        user_id=users["outsider"].id,
        role=ProjectRole.OWNER,
    )

    db_session.add_all(
        [
            owner_membership,
            member_membership,
            viewer_membership,
            other_member_membership,
            outsider_membership,
        ]
    )

    db_session.flush()

    # ----------------------------
    # Boards
    # ----------------------------

    board = Board(
        title="Tablero compartido",
        project_id=project.id,
        owner_id=users["owner"].id,
    )

    private_board = Board(
        title="Tablero privado",
        project_id=private_project.id,
        owner_id=users["outsider"].id,
    )

    db_session.add_all(
        [
            board,
            private_board,
        ]
    )

    db_session.flush()

    # ----------------------------
    # Task
    # ----------------------------

    task = Task(
        title="Tarea compartida",
        board_id=board.id,
    )

    db_session.add(task)
    db_session.flush()

    # ----------------------------
    # Comment
    # ----------------------------

    comment = Comment(
        content="Comentario del miembro",
        task_id=task.id,
        author_id=users["member"].id,
    )

    db_session.add(comment)

    db_session.commit()

    # ----------------------------
    # Refresh
    # ----------------------------

    db_session.refresh(project)
    db_session.refresh(private_project)

    db_session.refresh(owner_membership)
    db_session.refresh(member_membership)
    db_session.refresh(viewer_membership)
    db_session.refresh(other_member_membership)
    db_session.refresh(outsider_membership)

    db_session.refresh(board)
    db_session.refresh(private_board)

    db_session.refresh(task)
    db_session.refresh(comment)

    return {
        "project": project,
        "private_project": private_project,
        "board": board,
        "private_board": private_board,
        "task": task,
        "comment": comment,
        "owner_membership": owner_membership,
        "member_membership": member_membership,
        "viewer_membership": viewer_membership,
        "other_member_membership": other_member_membership,
        "outsider_membership": outsider_membership,
    }


# --------------------------------------------------
# ATTACHMENTS
# --------------------------------------------------


@pytest.fixture()
def attachment_fixture(
    db_session,
    authorization_data,
    users,
):

    os.makedirs("uploads", exist_ok=True)

    with open("uploads/manual.pdf", "wb") as file:
        file.write(b"Contenido de prueba")

    attachment = Attachment(
        filename="uuid-file.pdf",
        original_filename="manual.pdf",
        content_type="application/pdf",
        file_size=1024,
        storage_path="uploads/manual.pdf",
        task_id=authorization_data["task"].id,
        uploaded_by=users["owner"].id,
    )

    db_session.add(attachment)
    db_session.commit()
    db_session.refresh(attachment)

    yield attachment

    if os.path.exists("uploads/manual.pdf"):
        os.remove("uploads/manual.pdf")


# --------------------------------------------------
# ACTIVITY LOGS
# --------------------------------------------------


@pytest.fixture()
def activity_log_fixture(
    db_session,
    authorization_data,
    users,
):

    log = ActivityLog(
        action=ActivityAction.PROJECT_CREATED,
        entity_type="project",
        entity_id=authorization_data["project"].id,
        description="Proyecto creado",
        user_id=users["owner"].id,
        project_id=authorization_data["project"].id,
    )

    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    return log


# --------------------------------------------------
# NOTIFICATIONS
# --------------------------------------------------


@pytest.fixture()
def notification_fixture(
    db_session,
    authorization_data,
    users,
):

    notification = Notification(
        type=NotificationType.TASK_ASSIGNED,
        title="Nueva tarea",
        message="Se te asignó una tarea.",
        entity_type="task",
        entity_id=authorization_data["task"].id,
        recipient_id=users["member"].id,
        sender_id=users["owner"].id,
        project_id=authorization_data["project"].id,
    )

    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)

    return notification
