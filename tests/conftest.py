# set environment variable to override database location
# do this first so the override is used in the imports
import os
os.environ["FASTR_DATABASE_PATH"] = "./tests/test_db.sqlite"

import pytest
import requests

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sqlite3

from fastr.main import app
from fastr.db import models
from fastr.db.database import get_db, engine
from fastr.config import Settings


settings = Settings()


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def test_db() -> Session:
    """Set up and tear down the test database each time so each test starts with the
    same data."""
    # create the test database
    models.Base.metadata.create_all(bind=engine)

    # populate the test data
    db = sqlite3.connect(
        database=settings.database_path,
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.executescript(_data_sql)

    # yield TestingSessionLocal()
    yield next(get_db())

    # remove the database when finished
    os.unlink(settings.database_path)


@pytest.fixture
def client(test_db) -> TestClient:
    with TestClient(app) as c:
        yield c


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test") -> requests.Response:
        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password},
            allow_redirects=True,
        )

    def logout(self) -> requests.Response:
        return self._client.get("/auth/logout", allow_redirects=True)


@pytest.fixture
def auth(client) -> AuthActions:
    return AuthActions(client)
