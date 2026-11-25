import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from app import main

@pytest.fixture()
def client(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setattr(main, "DB_PATH", __import__("pathlib").Path(path))
    with TestClient(main.app) as test_client:
        yield test_client
    os.unlink(path)
