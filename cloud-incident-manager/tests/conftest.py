
from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db, get_engine
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    testing_session = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    def override_get_engine():
        return test_engine

    @asynccontextmanager
    async def test_lifespan(application):
        yield

    original_lifespan = app.router.lifespan_context

    app.router.lifespan_context = test_lifespan
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_engine] = override_get_engine

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.router.lifespan_context = original_lifespan

        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()
