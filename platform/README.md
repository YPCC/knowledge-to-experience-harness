# Mini YouTube Platform (React)

Professional, filterable video consumption experience for the Knowledge-to-Experience Agent Harness.

Built with Vite + React + TypeScript for a clean, modern look (not Streamlit/Gradio).

## Features

- Searchable video library with tag filtering
- Card grid with type badges and durations
- Player view with:
  - Video playback (when URL available)
  - Timestamped transcript
  - Side-by-side grounded chat (placeholder that cites source; ready for real Grok/transcript search)
- Dark professional theme, responsive
- Designed to load metadata JSON produced by the harness
- Generic: works for any source (GitHub repos, PowerPoint, papers, docs, videos)

## Run locally

```bash
cd platform
npm install
npm run dev
```

Then open the URL shown (usually http://localhost:5173).

## Sample data

Currently loads in-memory sample videos:
- Harness overview (with actual video path for local demo)
- CMS Policy-as-Code overview, business, and architecture placeholders (from https://github.com/YPCC/cms-policy-as-code)

In production the platform reads generated metadata JSON + video assets.

## Next

- Wire real video URLs / CDN
- Connect chat to transcript search + optional web exploration (clearly labeled)
- Playlist and related-videos recommendations
- Upload / publish hooks (YouTube API optional)
