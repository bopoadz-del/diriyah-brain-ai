# Full rewritten service file with real credentials and stub fallback
"""Google Drive helper functions with graceful stub fallbacks."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

logger = logging.getLogger(__name__)

__all__ = (
    "drive_credentials_available",
    "drive_service_error",
    "get_drive_service",
    "get_project",
    "list_project_folders",
    "upload_to_drive",
)

if TYPE_CHECKING:  # pragma: no cover - hinting only
    from fastapi import UploadFile
else:  # pragma: no cover - runtime fallback when FastAPI not available
    UploadFile = Any  # type: ignore[misc,assignment]

DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"

STUB_FILE_ID = "stub-file-0001"
STUB_FOLDERS: List[Dict[str, str]] = [
    {
        "id": "stub-folder-001",
        "name": "Gateway District Phase 1",
        "mimeType": "application/vnd.google-apps.folder",
    },
    {
        "id": "stub-folder-002",
        "name": "Bujairi Terrace Expansion",
        "mimeType": "application/vnd.google-apps.folder",
    },
]

_last_service_error: Optional[str] = None

def _credentials_path() -> Optional[Path]:
    env_value = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not env_value:
        return None
    candidate = Path(env_value).expanduser()
    if not candidate.is_file():
        return None
    if not os.access(candidate, os.R_OK):
        return None
    return candidate

def drive_credentials_available() -> bool:
    return _credentials_path() is not None

def drive_service_error() -> Optional[str]:
    return _last_service_error

def _record_service_error(reason: Optional[str]) -> None:
    global _last_service_error
    _last_service_error = reason

def get_drive_service() -> Any | None:
    credentials_path = _credentials_path()
    if not credentials_path:
        _record_service_error("GOOGLE_APPLICATION_CREDENTIALS missing or unreadable")
        return None

    try:
        from google.oauth2 import service_account  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except Exception as exc:
        logger.warning("Google Drive libraries unavailable: %s", exc)
        _record_service_error(str(exc))
        return None

    try:
        credentials = service_account.Credentials.from_service_account_file(
            str(credentials_path), scopes=[DRIVE_SCOPE]
        )
        service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        _record_service_error(None)
        return service
    except Exception as exc:
        logger.warning("Failed to initialise Google Drive service: %s", exc)
        _record_service_error(str(exc))
        return None

def upload_to_drive(
    file_obj: "UploadFile",
    *,
    service: Any | None = None,
    lookup_service: bool = True,
) -> str:
    if service is None and lookup_service:
        service = get_drive_service()
    if service is None:
        return STUB_FILE_ID

    try:
        from googleapiclient.http import MediaIoBaseUpload  # type: ignore

        metadata = {"name": getattr(file_obj, "filename", "upload.bin")}
        media = MediaIoBaseUpload(
            file_obj.file, mimetype=getattr(file_obj, "content_type", None), resumable=False
        )
        response = (
            service.files()
            .create(body=metadata, media_body=media, fields="id")
            .execute()
        )
        return response.get("id", STUB_FILE_ID)
    except Exception as exc:
        logger.warning("Drive upload failed, returning stub identifier: %s", exc)
        return STUB_FILE_ID

def list_project_folders(
    *, service: Any | None = None, lookup_service: bool = True
) -> List[Dict[str, Any]]:
    if service is None and lookup_service:
        service = get_drive_service()
    if service is None:
        return [folder.copy() for folder in STUB_FOLDERS]

    try:
        response = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id,name,mimeType)",
            )
            .execute()
        )
        return response.get("files", [])
    except Exception as exc:
        logger.warning("Drive list failed, returning stub folders: %s", exc)
        return list(STUB_FOLDERS)

def get_project(project_id: str) -> Dict[str, str]:
    return {
        "id": project_id,
        "name": f"Project {project_id}",
        "drive_id": "stub",
    }
