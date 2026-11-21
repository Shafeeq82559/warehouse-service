import pytest
from fastapi.testclient import TestClient

from warehouse.main import app
from warehouse.repository import store

HEADERS = {"X-API-Key": "dev-key"}


@pytest.fixture(autouse=True)
def clean_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def headers():
    return HEADERS
