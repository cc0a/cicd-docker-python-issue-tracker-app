import json

import boto3
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


def get_database_url():
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


database_url = get_database_url()

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()