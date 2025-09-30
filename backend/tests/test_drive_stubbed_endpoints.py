# Regression coverage for stubbed Google Drive behaviour
from __future__ import annotations
from pathlib import Path
from typing import Generator
import pytest
from fastapi.testclient import TestClient

from backend.api import projects
from backend.main import app
from backend.services import google_drive

@pytest.fixture()
def stubbed_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    missing_path = Path("/tmp/google-credentials-missing.json")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(missing_path))
    with TestClient(app) as test_client:
        yield test_client

def test_upload_endpoint_stubbed(stubbed_client: TestClient) -> None:
    response = stubbed_client.post(
        "/api/upload",
        files={"file": ("demo.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "stubbed"
    assert payload["file_id"] == google_drive.STUB_FILE_ID
    assert payload["detail"] == google_drive.drive_service_error()
