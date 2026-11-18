# YouTube Configuration

Optional. Used only when you want to publish generated videos.

## Setup

1. Create a Google Cloud project and enable YouTube Data API v3.
2. Create an OAuth 2.0 Client ID (Desktop app) and download the JSON.
3. Save it as `client_secrets.json` in the repo root (or set `YOUTUBE_CLIENT_SECRETS`).
4. Copy the example:

   ```bash
   cp config/youtube.example.json config/youtube.json
   ```

5. Obtain a token (one-time browser consent):

   ```bash
   python3 scripts/youtube_oauth_stub.py
   ```

6. Default privacy is `private`. Change in `config/youtube.json` or via `YOUTUBE_PRIVACY`.

## Publish

From the generator console or via API:

```bash
curl -X POST http://localhost:8765/api/youtube/publish \
  -H 'Content-Type: application/json' \
  -d '{"id": "overview"}'
```

Or check status:

```bash
curl http://localhost:8765/api/youtube/status
```

Credentials stay on your machine and are never committed.
