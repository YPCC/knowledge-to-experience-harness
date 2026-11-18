# Knowledge-to-Experience Harness · Generator Console

Professional McKinsey-style local interface with **real backend calls**.

## One-time setup (macOS or Windows)

From the repository root:

```bash
python3 scripts/setup_environment.py
```

The script detects your OS and:
- Installs Python packages (`pdfplumber`, `python-pptx`)
- Installs **ffmpeg** (Homebrew on macOS, winget/Chocolatey on Windows)
- Optionally installs Node.js (for the React platform)
- Creates the `uploads/` and `generated/` directories

## Start the backend

```bash
python3 scripts/generator_server.py
```

Then open **http://localhost:8765** in your browser.

The server:
- Serves the UI
- Accepts file uploads (PDF, PPTX, Markdown) or GitHub URLs
- Runs real text extraction (pdfplumber / python-pptx)
- Writes candidate plans, metadata JSON, transcripts, and short ffmpeg videos into `artifacts/generated/`
- Stores feedback as `{video_id}.feedback.json`

## UI workflow

1. **Setup** — detects backend and reports tool availability
2. **Ingest** — drag-and-drop or paste URL → real `/api/ingest`
3. **Review Plan** — select candidates
4. **Generate** — real `/api/generate` writes artifacts
5. **Videos & Feedback** — review + submit feedback (stored on disk)

If the backend is not running, the UI falls back to simulation mode and tells you how to start it.

## Artifacts written

```
artifacts/generated/
  {source}.plan.json
  {video_id}.metadata.json
  {video_id}.timestamps.json
  {video_id}.mp4          (short placeholder video)
  {video_id}.feedback.json
```

## Dependencies

- Python 3.10+ (stdlib only for the server)
- `pdfplumber`, `python-pptx` (installed by setup script)
- ffmpeg (installed by setup script)
