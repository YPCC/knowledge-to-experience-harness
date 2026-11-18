# Knowledge-to-Experience Harness

Reusable pipeline that turns source material — GitHub repositories, papers, PowerPoint, PDFs, or document sets — into short educational/demo videos, transcripts, metadata, and an interactive consumption experience with grounded chat.

---

## Quick Start

```bash
git clone https://github.com/YPCC/knowledge-to-experience-harness.git
cd knowledge-to-experience-harness

# One-time setup (detects macOS / Windows and installs prerequisites)
python3 scripts/setup_environment.py

# Start the generator console
python3 scripts/generator_server.py
```

Open **http://localhost:8765**.

Follow the five steps in the browser:

1. **Setup** — confirm the backend and tools are ready
2. **Ingest** — drag-and-drop a PDF/PPTX/Markdown or paste a GitHub URL
3. **Review Plan** — select the candidate videos
4. **Generate** — the backend writes real artifacts
5. **Videos & Feedback** — review outputs and submit refinement notes

Outputs appear in `generated/`.

---

## Detailed Steps

### 1. Run the setup script

```bash
python3 scripts/setup_environment.py
```

The script detects your operating system and installs only what is missing:

| Component | macOS | Windows |
|-----------|-------|---------|
| Python packages (`pdfplumber`, `python-pptx`) | pip | pip |
| ffmpeg | Homebrew | winget or Chocolatey |
| Node.js (optional, for React platform) | Homebrew | winget |
| Working directories | created | created |

Safe to re-run. Existing tools are skipped.

### 2. Start the generator backend

```bash
python3 scripts/generator_server.py
```

The server:
- Serves the McKinsey-style web UI
- Accepts file uploads and GitHub URLs
- Performs real text extraction
- Writes plans, metadata, transcripts, short videos, and feedback into `generated/`

Leave the terminal open. The UI is at **http://localhost:8765**.

### 3. (Optional) Configure an LLM backend

For full generation and chat:

```bash
cp .env.example .env
# edit .env
```

See [docs/llm-configuration.md](docs/llm-configuration.md) for Gemini, Grok/xAI, or Vertex AI (ADC).

### 4. (Optional) Open the consumption platform

```bash
cd platform
npm install
npm run dev
```

Professional React viewer with search, tag filtering, playback, transcript view, and grounded chat.

---

## Generated Artifacts

```
generated/
  {source}.plan.json          # Candidate video plan
  {video_id}.metadata.json    # Title, type, tags, provenance
  {video_id}.timestamps.json  # Transcript with timestamps
  {video_id}.mp4              # Short video
  {video_id}.feedback.json    # User feedback for refinement
```

---

## Core Pipeline

1. **Source Ingestion** — GitHub repo / video URL / paper / docs / PPTX / PDF → structured summary + candidate video topics
2. **Video Generation** — Scripts (overview, deep-dive, dialogue, short explainer, how-it-works) → multi-speaker voice → visuals + ffmpeg assembly → MP4 + MP3 + timestamped transcript
3. **Tagging & Metadata** — Manual + AI tags, short description, key timestamps, concept links, JSON metadata. Provenance tracked (source commit/URL, prompts, settings)
4. **Chat Interface** — Grounded Q&A over transcripts (jump to timestamps, cite source sections). Separate concept-exploration chat that can browse the web
5. **Consumption Platform** — Professional React (Vite + TypeScript) filterable video browser. Playback + transcript + grounded chat side-by-side

---

## Project Structure

| Path | Purpose |
|------|---------|
| `scripts/setup_environment.py` | Cross-platform prerequisite installer |
| `scripts/generator_server.py` | Local backend for the generator console |
| `generator-ui/` | McKinsey-style web UI (served by the backend) |
| `platform/` | React consumption experience |
| `docs/` | Skills, ingestion notes, evaluation framework, source plans |
| `docs/skills/` | Reusable skill documents (voice, visual-style, tagging) |
| `skills/open-code-review/` | Code-review skill for any Git repository |
| `videos/` | Example generated videos |
| `generated/` | Output plans, metadata, transcripts, videos, feedback |
| `uploads/` | Temporary storage for uploaded source files |
| `config/` | LLM provider configuration examples |

---

## Example Videos

### Harness Overview
What is the Knowledge-to-Experience Harness? (~63 s)  
[View](https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/k2e_harness_overview_v1.mp4)

### CMS Policy-as-Code Series
Generated from [cms-policy-as-code](https://github.com/YPCC/cms-policy-as-code):

- Overview (~59 s) — [view](https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_overview_v1.mp4)
- Business (~47 s) — [view](https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_business_v1.mp4)
- Architecture (~53 s) — [view](https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_architecture_v1.mp4)
- How it works (~42 s) — [view](https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_howitworks_v1.mp4)

Candidate plan: `docs/sources/cms-policy-as-code-plan.md`

### SemRep Multi-Source Example
Business overview (~53 s) and technical deep dive (~63 s) combining a web page, GitHub repository, knowledge-graph registry, research paper, and PowerPoint.  
Guide: [docs/semrep-multisource-guide.md](docs/semrep-multisource-guide.md)

---

## Why This Exists

- Turn raw technical and business knowledge into consumable, visual learning experiences
- Keep outputs grounded, traceable, and free of invented sensitive data
- Modular stages that can be run or re-run independently
- Searchable mini-YouTube-style browser with grounded chat
- Integrable with Grok, Gemini, or Vertex AI

---

## Code Review

The skill at `skills/open-code-review/` can review any Git repository using [alibaba/open-code-review](https://github.com/alibaba/open-code-review).

```bash
npm install -g @alibaba-group/open-code-review
ocr config provider
ocr review --audience agent --background "context" --format json
```

See `skills/open-code-review/SKILL.md` for the full workflow.

---

## Operating Principles

- Prefer synthetic or publicly available source material
- Produce reusable artifacts (scripts, transcripts, metadata JSON, `.mp4`)
- Keep generation modular
- Record provenance with each output

---

## Next Steps

Implemented in this update:

- Multi-speaker voice and visual stages wired into the generator backend (`scripts/generation_stages.py`)
- Automated evaluation of clarity and technical accuracy (`scripts/evaluation.py`), results stored in metadata
- Consumption platform loads from `generated/` when the backend is running (falls back to static `videos.json`)
- YouTube publish path with config-based credentials (`scripts/youtube_publish.py`, `config/youtube.example.json`, `docs/youtube-config.md`)

Remaining:

- Swap the voice stage for a live TTS provider when credentials are present
- Expand visual generation beyond title cards
- YouTube resumable upload refinements
