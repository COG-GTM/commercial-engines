import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db as db_module
from app.db import Base, get_db
from app.main import app
from app.seed import seed


@pytest.fixture()
def client(tmp_path):
    test_engine = create_engine(
        f"sqlite:///{tmp_path/'test.db'}", connect_args={"check_same_thread": False}
    )
    TestingSession = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(test_engine)
    with TestingSession() as s:
        seed(s)

    def override_get_db():
        s = TestingSession()
        try:
            yield s
        finally:
            s.close()

    # Neutralise the lifespan seeding against the default engine.
    db_module.engine = test_engine
    db_module.SessionLocal = TestingSession
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
