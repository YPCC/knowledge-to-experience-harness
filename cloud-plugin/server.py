#!/usr/bin/env python3
"""
Knowledge-to-Experience Cloud Plugin (MCP Server)

Turns any source (GitHub URL, paper URL, document text, or file) into short educational videos.
By default generates Executive (business overview) and Technical (architecture) videos.
Video types can be overridden via the instruction/prompt.

Run as MCP server (stdio or HTTP):
  python cloud-plugin/server.py

Or with FastMCP HTTP for cloud:
  fastmcp run cloud-plugin/server.py --transport sse --port 8000
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Ensure we can import from the repo's scripts/
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

try:
    from generation_stages import run_stages
    from evaluation import run_evaluation
except ImportError as e:
    print(f"Warning: could not import generation stages: {e}")
    run_stages = None
    run_evaluation = None

try:
    from fastmcp import FastMCP
except ImportError:
    print("fastmcp not installed. Install with: pip install fastmcp")
    sys.exit(1)

mcp = FastMCP(
    name="Knowledge-to-Experience Harness",
    instructions=(
        "Generate short educational/demo videos (executive + technical by default) "
        "from any source: GitHub repository, paper, document, or raw text. "
        "Provide a source URL or text and an optional instruction describing desired video types."
    ),
)

DEFAULT_VIDEOS = [
    {
        "id": "executive",
        "title": "Executive Overview",
        "type": "overview",
        "duration": "45–60s",
        "outline": "Problem context, key capabilities, business value, and high-level outcomes for decision-makers."
    },
    {
        "id": "technical",
        "title": "Technical Deep Dive",
        "type": "technical",
        "duration": "50–70s",
        "outline": "System structure, core components, data flow, architecture, and integration points."
    },
]

def _select_videos(instruction: Optional[str]) -> List[Dict[str, Any]]:
    """Select video types based on instruction; default to executive + technical."""
    if not instruction:
        return DEFAULT_VIDEOS
    instr = instruction.lower()
    selected = []
    if any(k in instr for k in ["executive", "business", "overview", "summary", "decision"]):
        selected.append(DEFAULT_VIDEOS[0])
    if any(k in instr for k in ["technical", "architecture", "deep dive", "deep-dive", "how it works", "engineering"]):
        selected.append(DEFAULT_VIDEOS[1])
    if "dialogue" in instr or "conversation" in instr:
        selected.append({
            "id": "dialogue",
            "title": "Concept Dialogue",
            "type": "dialogue",
            "duration": "55–75s",
            "outline": "Multi-speaker conversation exploring trade-offs and design rationale."
        })
    if "how it works" in instr or "walkthrough" in instr:
        selected.append({
            "id": "howitworks",
            "title": "How It Works",
            "type": "walkthrough",
            "duration": "40–55s",
            "outline": "Step-by-step walkthrough of the primary workflow."
        })
    return selected or DEFAULT_VIDEOS

def _fetch_source_text(source: str) -> str:
    """Best-effort text extraction from URL or raw text."""
    if source.startswith(("http://", "https://")):
        try:
            import httpx
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                r = client.get(source)
                r.raise_for_status()
                content = r.text
                # Prefer README if GitHub
                if "github.com" in source and "/raw/" not in source:
                    # Try to append a note; full clone is out of scope for the plugin stub
                    content = f"Source URL: {source}\n\n{content[:8000]}"
                return content[:20000]
        except Exception as e:
            return f"[Could not fetch {source}: {e}]"
    return source[:20000]

@mcp.tool
def generate_videos(
    source: str,
    instruction: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate educational videos from a source.

    Args:
        source: GitHub URL, paper URL, document text, or any content string.
        instruction: Natural-language description of desired videos
                     (e.g. "executive overview and technical architecture").
                     Defaults to executive + technical if omitted.
        output_dir: Directory to write artifacts (default: ./generated or /tmp/k2e-generated).

    Returns:
        Metadata for generated videos, including paths and transcripts.
    """
    if run_stages is None:
        return {"error": "Generation stages not available. Run from the repository root."}

    out = Path(output_dir or os.environ.get("K2E_OUTPUT_DIR", "/tmp/k2e-generated"))
    out.mkdir(parents=True, exist_ok=True)

    source_text = _fetch_source_text(source)
    videos_to_make = _select_videos(instruction)

    results = []
    for item in videos_to_make:
        # Enrich title with source stem if possible
        stem = Path(source.split("/")[-1] or "source").stem
        item = dict(item)
        item["title"] = f"{stem} · {item['title']}"

        stage_result = run_stages(item, source_text, out)
        vid_id = stage_result["id"]
        script = stage_result["script"]
        voice = stage_result["voice"]

        eval_result = {}
        if run_evaluation:
            eval_result = run_evaluation(vid_id, script, voice.get("turns", []), source_text, out)

        meta = {
            "id": vid_id,
            "title": item["title"],
            "type": item["type"],
            "description": item["outline"],
            "duration": item["duration"],
            "source": source,
            "instruction": instruction or "default (executive + technical)",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "status": "ready",
            "tags": [item["type"], "generated", "harness", "cloud-plugin"],
            "transcript": voice.get("turns", []),
            "speakers": voice.get("speakers", []),
            "evaluation": eval_result,
            "video_path": stage_result.get("video_path"),
            "artifacts_dir": str(out),
        }
        meta_path = out / f"{vid_id}.metadata.json"
        meta_path.write_text(json.dumps(meta, indent=2))
        results.append(meta)

    return {
        "ok": True,
        "source": source,
        "instruction": instruction,
        "videos": results,
        "output_dir": str(out),
        "note": "Videos are short title-card assemblies. Configure LLM + TTS for full narration."
    }

@mcp.tool
def list_default_video_types() -> Dict[str, Any]:
    """Return the default video types produced by the plugin."""
    return {
        "default": DEFAULT_VIDEOS,
        "available_keywords": ["executive", "business", "technical", "architecture", "dialogue", "how it works", "walkthrough"]
    }

if __name__ == "__main__":
    # Default: stdio transport for local MCP clients (Claude Desktop, Cursor, etc.)
    # For cloud HTTP/SSE: use `fastmcp run cloud-plugin/server.py --transport sse --port 8000`
    mcp.run()
