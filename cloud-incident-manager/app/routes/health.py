from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine

router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("/")
def health_check():
    return {"status": "healthy", "application": "Cloud Incident Manager"}


@router.get("/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "connected", "database": "available"}

    except SQLAlchemyError:
        return {"status": "error", "database": "unavailable"}
