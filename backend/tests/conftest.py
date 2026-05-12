import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("FRONTEND_ORIGIN", "http://localhost:4321")
os.environ.setdefault("SESSION_SECRET_KEY", "test-session-secret-key")
os.environ.setdefault("SESSION_TTL_SECONDS", "3600")

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Real test client with actual services (no mocks)."""
    return TestClient(app)