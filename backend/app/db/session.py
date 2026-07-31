from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Crea una sesión de base de datos y la cierra
    automáticamente al finalizar la petición.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()