import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Real test client with actual services (no mocks)."""
    return TestClient(app)