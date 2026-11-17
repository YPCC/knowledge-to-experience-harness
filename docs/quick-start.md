# Quick Start Guide — Knowledge-to-Experience Agent Harness

Get the harness running and start turning your own sources (GitHub repos, PDFs, PowerPoints, papers, or documents) into short educational videos, metadata, and an interactive experience.

This guide covers installation, the current modular workflow, and a concrete walkthrough using the existing **CMS Policy-as-Code** video series as the example.

## Prerequisites

- **Git**
- **Python 3.10+** (for ingestion scripts)
- **Node.js 18+ & npm** (only if you want to run the React mini-platform locally)
- **ffmpeg** (for video assembly; optional for viewing existing videos)
- Optional: Grok (or equivalent) access for script generation, narration coordination, and grounded chat

## 1. Install / Clone the Repository

```bash
git clone https://github.com/YPCC/knowledge-to-experience-harness.git
cd knowledge-to-experience-harness
```

No global package install is required yet. The harness is currently a modular collection of:

- Reusable **skill documents** (`docs/skills/`)
- Ingestion stubs (`scripts/`)
- Example videos (`videos/`)
- Metadata and platform scaffolding (`platform/`)
- Provenance and plans (`docs/`)

You work with it by combining these pieces with an agent (Grok recommended) that follows the skill documents.

## 2. View Existing Videos Immediately

All generated videos live in the `videos/` folder and are also embedded in the root README.

Example (CMS series):

```bash
# Play locally (requires a media player that handles MP4)
open videos/cms_policy_overview_v1.mp4          # macOS
# or
vlc videos/cms_policy_overview_v1.mp4           # or any player
```

Direct raw links (also work in browsers):

- Overview: https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_overview_v1.mp4
- Business: https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_business_v1.mp4
- Architecture: https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_architecture_v1.mp4
- How it works: https://github.com/YPCC/knowledge-to-experience-harness/raw/main/videos/cms_policy_howitworks_v1.mp4

## 3. Run the Mini-YouTube Platform (Optional)

The React platform is scaffolded under `platform/`. The full interactive source is still evolving; currently `platform/public/videos.json` contains the metadata for the harness overview + CMS series.

```bash
cd platform
npm install          # once the full Vite + React source is committed
npm run dev
```

Then open http://localhost:5173. Videos are expected under paths referenced in `videos.json` (adjust or copy MP4s into `platform/public/` as needed).

## 4. Start Working with Any File or Artifact

### Option A — PDF or PowerPoint (fastest local start)

```bash
# Install minimal dependencies if needed
pip install pdfplumber python-pptx

python scripts/ingest_stub.py path/to/your-document.pdf
# or
python scripts/ingest_stub.py path/to/your-slides.pptx
```

This produces a `*.plan.json` with candidate video topics (Overview, Technical, Business, How-it-works). Review and refine the plan, then proceed to script generation using the skill documents.

### Option B — GitHub Repository (primary path)

1. Point the agent at the repository URL (e.g. `https://github.com/your-org/your-repo`).
2. The agent produces a source summary + candidate video plan (see `docs/sources/cms-policy-as-code-plan.md` for the format).
3. Generate scripts following `docs/skills/voice.md` and `docs/skills/visual-style.md`.
4. Assemble video (voice + visuals + ffmpeg) and emit metadata JSON + transcript.
5. Register the new entry in `platform/public/videos.json` (or your own metadata store).

### Option C — Existing Video, Paper, or Document Set

Follow `docs/ingestion-path.md`. Extract text/structure, produce a plan, then generate.

## 5. Showcase Example — CMS Policy-as-Code Series

**Source repository**: https://github.com/YPCC/cms-policy-as-code  
**Plan**: `docs/sources/cms-policy-as-code-plan.md`  
**Generated videos** (all under `videos/`):

| Video | Length | Type | Focus |
|-------|--------|------|-------|
| `cms_policy_overview_v1.mp4` | ~59s | Overview | Unstructured docs → auditable rules |
| `cms_policy_business_v1.mp4` | ~47s | Business | Why it matters for payers |
| `cms_policy_architecture_v1.mp4` | ~53s | Technical | Neuro-symbolic pipeline |
| `cms_policy_howitworks_v1.mp4` | ~42s | How-it-works | Claim → Decision Trace |

**How this was produced (repeatable pattern)**:

1. Ingest the source repo → concise summary + candidate topics (recorded in the plan file).
2. Write scripts for each type using the voice and visual-style skills.
3. Generate narration (multi-speaker when useful) + simple slide visuals.
4. Assemble with ffmpeg → MP4 + matching transcript with timestamps.
5. Create metadata entries (see `platform/public/videos.json`) including tags, description, source URL, and transcript snippets.
6. Embed or load into the consumption platform for search, playback, and grounded chat.

**Try it yourself**:

- Open any of the four CMS videos.
- Look at the corresponding transcript fragments in `platform/public/videos.json`.
- Ask a grounded question about the content (e.g., “What is a Decision Trace?”) — the platform or an agent using the transcript should cite the relevant timestamp.
- Clone the source repo and repeat the plan → script → video steps for a new topic.

## 6. Next Actions After Quick Start

- Review `docs/skills/` and adapt voice/visual style to your brand.
- Run `scripts/ingest_stub.py` on one of your own PDFs or PPTXs.
- Generate your first overview video following the CMS pattern.
- Update `docs/generation-log.md` with your run.
- Optionally explore YouTube publishing notes in `docs/youtube-publish-notes.md`.

**Knowledge in. Trusted experiences out.**

For questions or contributions, open an issue or follow the operating principles in the root README.
