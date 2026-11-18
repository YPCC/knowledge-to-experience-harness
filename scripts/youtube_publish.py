#!/usr/bin/env python3
"""
YouTube publish path.

Credentials are read from environment or a local config file (never committed).
Supports:
  - YOUTUBE_CLIENT_SECRETS path
  - YOUTUBE_TOKEN path
  - Optional privacy status (private by default)

Does not upload unless explicitly invoked and credentials are present.
"""

import os
import json
from pathlib import Path
from datetime import datetime

CONFIG_PATH = Path(os.environ.get("YOUTUBE_CONFIG", "config/youtube.json"))
CLIENT_SECRETS = os.environ.get("YOUTUBE_CLIENT_SECRETS", "client_secrets.json")
TOKEN_FILE = os.environ.get("YOUTUBE_TOKEN", "youtube_token.json")

def load_config() -> dict:
    cfg = {
        "client_secrets": CLIENT_SECRETS,
        "token_file": TOKEN_FILE,
        "privacy": os.environ.get("YOUTUBE_PRIVACY", "private"),
        "category_id": os.environ.get("YOUTUBE_CATEGORY", "22"),
    }
    if CONFIG_PATH.exists():
        try:
            file_cfg = json.loads(CONFIG_PATH.read_text())
            cfg.update(file_cfg)
        except Exception:
            pass
    return cfg

def is_configured() -> bool:
    cfg = load_config()
    return Path(cfg["client_secrets"]).exists() or Path(cfg["token_file"]).exists()

def publish_video(video_path: Path, title: str, description: str, tags: list | None = None) -> dict:
    """Attempt to publish. Returns status dict. Requires google-api-python-client and valid OAuth."""
    cfg = load_config()
    if not Path(video_path).exists():
        return {"ok": False, "error": "video file not found"}
    if not is_configured():
        return {
            "ok": False,
            "error": "YouTube not configured",
            "hint": "Set YOUTUBE_CLIENT_SECRETS or place config/youtube.json. Run scripts/youtube_oauth_stub.py to obtain a token."
        }
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        return {
            "ok": False,
            "error": "YouTube client libraries missing",
            "hint": "pip install google-api-python-client google-auth-oauthlib google-auth-httplib2"
        }

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None
    token_path = Path(cfg["token_file"])
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            secrets = Path(cfg["client_secrets"])
            if not secrets.exists():
                return {"ok": False, "error": f"Missing client secrets: {secrets}"}
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets), scopes)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags or ["knowledge-to-experience", "harness"],
            "categoryId": cfg["category_id"]
        },
        "status": {"privacyStatus": cfg["privacy"]}
    }
    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    return {
        "ok": True,
        "video_id": response.get("id"),
        "url": f"https://youtu.be/{response.get('id')}",
        "privacy": cfg["privacy"],
        "published_at": datetime.utcnow().isoformat() + "Z"
    }

def status() -> dict:
    return {
        "configured": is_configured(),
        "config_path": str(CONFIG_PATH),
        "client_secrets_exists": Path(CLIENT_SECRETS).exists(),
        "token_exists": Path(TOKEN_FILE).exists(),
        "privacy_default": load_config()["privacy"]
    }
