import traceback
from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.settings import get_settings
from app.services.logger_service import LoggerService

settings = get_settings()
logger = LoggerService()

SQLALCHEMY_DATABASE_URL = settings.database_url

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Verifica conexiones antes de usarlas
        pool_size=10,  # Tamaño máximo del pool
        max_overflow=20,  # Conexiones adicionales permitidas
        pool_recycle=3600,  # Recicla conexiones después de una hora
    )
except Exception as e:
    logger.log(
        entry={
            "error": "Error al crear el engine de la base de datos",
            "details": str(e),
            "traceback": traceback.format_exc(),
        },
        filename="db_errors",
    )
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.log(
            entry={
                "error": "Error en la sesión de base de datos",
                "details": str(e),
                "traceback": traceback.format_exc(),
            },
            filename="db_errors",
        )
        raise
    finally:
        db.close()


@asynccontextmanager
async def get_async_db():
    """Contexto asíncrono para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.log(
            entry={
                "error": "Error en la sesión asíncrona de base de datos",
                "details": str(e),
                "traceback": traceback.format_exc(),
            },
            filename="db_errors",
        )
        raise
    finally:
        db.close()


def create_new_db_session():
    """Crea una nueva sesión de base de datos."""
    try:
        return SessionLocal()
    except SQLAlchemyError as e:
        logger.log(
            entry={
                "error": "Error al crear nueva sesión de base de datos",
                "details": str(e),
                "traceback": traceback.format_exc(),
            },
            filename="db_errors",
        )
        raise
