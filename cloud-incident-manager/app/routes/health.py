
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_engine

router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "application": "Cloud Incident Manager",
    }


@router.get("/database")
def database_health(engine: Engine = Depends(get_engine)):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": "available",
        }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "unavailable",
            },
        ) from exc
