# Knowledge-to-Experience Agent Harness

**From knowledge elements to trusted, interactive learning experiences.**

One Platform. Many Knowledge Elements. Greater Impact.

This repository is the open starting point for a reusable, modular **Knowledge-to-Experience (K2E) Agent Harness**.
It turns source material — primarily GitHub repositories, papers, documents, or videos — into polished short educational/demo videos (1–2 minutes, in the spirit of 3Blue1Brown), rich metadata, tags, and an interactive consumption experience with grounded chat.

Inspired by enterprise agent harness concepts (e.g., CitiusTech-style Knowledge-to-Experience diagrams) and modern agentic pipelines.

## Why This Exists

- Turn raw technical/business knowledge into consumable, visual, trusted learning experiences.
- Grounded, traceable, and governable (no invented PHI or proprietary data).
- Modular so individual stages (ingest, script, voice, visuals, tagging, platform) can be run independently.
- Searchable mini-YouTube-style browser + chat (grounded in transcripts + optional web exploration).
- Integrable with Grok or similar models for chat over the content.

## Core Pipeline

1. **Source Ingestion** — GitHub repo / video URL / paper / docs → structured summary + candidate video topics.
2. **Video Generation** — Scripts (overview, deep-dive, dialogue, short explainer, how-it-works) → multi-speaker voice → visuals + ffmpeg assembly → MP4 + MP3 + timestamped transcript.
3. **Tagging & Metadata** — Manual + AI tags, short description, key timestamps, concept links, JSON metadata record. Provenance tracked (source commit/URL, prompts, settings).
4. **Chat Interface** — Grounded Q&A over transcripts (jump to timestamps, cite source sections). Separate concept-exploration chat that can browse the web.
5. **Consumption Platform** — Lightweight filterable video browser (search, tags, playlists, related). Playback + transcript + chat side-by-side. Starts as Streamlit/Gradio; can grow or publish to YouTube.

## Short Plan — First Batch of Videos (Meta: Explaining the Harness Itself)

| # | Title | Type | Length | Focus |
|---|-------|------|--------|-------|
| 1 | What is the Knowledge-to-Experience Harness? | Overview | 60–90s | High-level value, inputs → outputs |
| 2 | Inside the Agent Harness (C4 Level 2) | Technical deep-dive | 90–120s | Planning loop, ingestion, generation, chat, evaluation |
| 3 | From GitHub Repo to 90-Second Explainer | How-it-works | 60–90s | End-to-end walkthrough on a sample public repo |
| 4 | Grounded Chat + Mini YouTube | Demo | 60s | Searching, timestamp jumps, Grok-style interaction |
| 5 | 3Blue1Brown-Style Visual Principles | Style guide | 60s | Clarity, visual metaphor, progressive disclosure |

Additional specialized videos will be generated per source (business aspect + technical aspect).

## Operating Principles

- Prefer synthetic or publicly available source material.
- Always emit reusable artifacts: scripts, transcripts, metadata JSON, intermediate audio.
- Version and provenance for every generated video.
- Modular skill documents for voice, visual style, captioning, branding.
- When a new GitHub link is provided, produce a short plan (candidate videos + outline) before generating assets.

## Repository Structure (evolving)

```
/
├── README.md
├── docs/
│   ├── architecture.md          # C4 diagrams & notes
│   ├── skills/                  # Reusable skill documents
│   │   ├── voice.md
│   │   ├── visual-style.md
│   │   └── tagging.md
│   └── generation-log.md
├── examples/
│   └── sample-source/           # Placeholder for first source
├── platform/                  # Mini YouTube / Streamlit app (coming)
├── scripts/                    # Generation scripts & prompts
└── artifacts/                  # Generated videos, transcripts, metadata (gitignored for large files)
```

## Next Steps

- [ ] Flesh out skill documents (voice, visual style matching 3B1B clarity).
- [ ] Implement first ingestion + script generation on a public GitHub source.
- [ ] Generate sample 60-second overview video.
- [ ] Scaffold Streamlit mini-platform with transcript search + chat stub.
- [ ] Research YouTube upload / API and Grok integration points.
- [ ] Evaluation framework for clarity and technical accuracy.

## Tech Notes

- Visuals: slide-based + generated imagery + ffmpeg (Manim-style where feasible).
- Voice: multi-speaker TTS.
- Chat: grounded on transcripts + optional external search.
- Platform: start lightweight (Streamlit), designed to grow or export.

**Knowledge in. Trusted experiences out.**

People | Technology | Impact
