
import json
from functools import lru_cache

import boto3
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


def get_database_url():
    # Local development and CI use the supplied database URL.
    if settings.database_url:
        return settings.database_url

    # Production retrieves credentials from AWS Secrets Manager.
    if not settings.database_secret_arn:
        raise RuntimeError(
            "Set DATABASE_URL or DATABASE_SECRET_ARN to configure the database."
        )

    client = boto3.client(
        "secretsmanager",
        region_name=settings.aws_region,
    )

    response = client.get_secret_value(
        SecretId=settings.database_secret_arn
    )

    secret = json.loads(response["SecretString"])

    return URL.create(
        drivername="postgresql+psycopg",
        username=secret["username"],
        password=secret["password"],
        host=secret["host"],
        port=int(secret["port"]),
        database=secret.get("dbname", "incidentdb"),
    )


@lru_cache(maxsize=1)
def get_engine():
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )


@lru_cache(maxsize=1)
def get_session_factory():
    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
    )


def get_db():
    db = get_session_factory()()

    try:
        yield db
    finally:
        db.close()
