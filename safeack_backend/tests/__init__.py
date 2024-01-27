from safeack_backend.api import app
from fastapi.testclient import TestClient

client = TestClient(app)
