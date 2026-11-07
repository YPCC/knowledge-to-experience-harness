#!/usr/bin/env python3
"""
YouTube OAuth stub for the Knowledge-to-Experience Harness.
User provides client_secrets.json. This handles the consent flow and stores credentials.
Does not perform uploads by default — just demonstrates the auth path.
"""

import os
import sys
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS = os.environ.get("YOUTUBE_CLIENT_SECRETS", "client_secrets.json")
TOKEN_FILE = "youtube_token.json"

def get_authenticated_service():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("Install dependencies: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
        sys.exit(1)

    creds = None
    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not Path(CLIENT_SECRETS).exists():
                print(f"Missing {CLIENT_SECRETS}. Download OAuth client secrets from Google Cloud Console.")
                print("Enable YouTube Data API v3 and create OAuth 2.0 Client ID (Desktop or Web).")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        Path(TOKEN_FILE).write_text(creds.to_json())
    print("Authentication successful. Token stored in", TOKEN_FILE)
    print("Note: Unverified projects can only upload private videos.")
    return creds

def main():
    print("YouTube OAuth stub for Knowledge-to-Experience Harness")
    print("Scopes:", SCOPES)
    get_authenticated_service()
    print("\nNext: use the credentials with videos.insert (resumable upload) to publish.")
    print("See docs/youtube-publish-notes.md for full flow.")

if __name__ == "__main__":
    main()
