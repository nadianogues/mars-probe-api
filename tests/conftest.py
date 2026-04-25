import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import probe_service


@pytest.fixture(autouse=True)
def clear_probes():
    probe_service._probes.clear()
    yield
    probe_service._probes.clear()


@pytest.fixture
def client():
    return TestClient(app)
