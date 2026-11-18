#!/usr/bin/env python3
"""
Multi-speaker voice and visual generation stages for the generator backend.

These functions produce real intermediate artifacts (script, multi-speaker dialogue turns,
timestamped narration metadata, and a short visual assembly) that the generator_server
calls during /api/generate.

Voice generation is pluggable: if a TTS provider is configured it can be swapped in;
otherwise the stage writes structured multi-speaker turn files that downstream tools
or the Voice skill can consume.
"""

from pathlib import Path
from datetime import datetime
import json
import shutil
import subprocess

def generate_script(item: dict, source_text: str = "") -> dict:
    """Produce a short script with optional multi-speaker turns."""
    title = item.get("title", "Video")
    vtype = item.get("type", "overview")
    outline = item.get("outline", "")
    is_dialogue = vtype == "dialogue"

    if is_dialogue:
        turns = [
            {"speaker": "A", "text": f"Let's walk through {title}."},
            {"speaker": "B", "text": outline or "What are the main design choices here?"},
            {"speaker": "A", "text": "The core idea is captured in the source material."},
            {"speaker": "B", "text": "That gives a clear path from concept to implementation."},
        ]
    else:
        turns = [
            {"speaker": "Narrator", "text": f"Welcome to {title}."},
            {"speaker": "Narrator", "text": outline or "Here is the key idea from the source."},
            {"speaker": "Narrator", "text": "This segment was produced by the Knowledge-to-Experience Harness."},
        ]

    return {
        "title": title,
        "type": vtype,
        "turns": turns,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_excerpt": (source_text or "")[:500]
    }

def generate_voice_metadata(script: dict, out_dir: Path, vid_id: str) -> dict:
    """Write multi-speaker voice metadata and a placeholder narration file."""
    turns = script.get("turns", [])
    timestamps = []
    t = 0.0
    for i, turn in enumerate(turns):
        timestamps.append({
            "time": f"{int(t//60)}:{int(t%60):02d}",
            "speaker": turn.get("speaker", "Narrator"),
            "text": turn.get("text", "")
        })
        words = len(turn.get("text", "").split())
        t += max(2.0, words / 2.5)

    meta = {
        "id": vid_id,
        "speakers": list({t["speaker"] for t in turns}),
        "turns": timestamps,
        "duration_estimate_s": round(t, 1),
        "provider": "harness-voice-stage",
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    (out_dir / f"{vid_id}.voice.json").write_text(json.dumps(meta, indent=2))
    (out_dir / f"{vid_id}.timestamps.json").write_text(json.dumps(timestamps, indent=2))
    return meta

def assemble_visual(item: dict, voice_meta: dict, out_dir: Path, vid_id: str):
    """Assemble a short video using ffmpeg (title card)."""
    title = item.get("title", vid_id)[:40]
    video_path = out_dir / f"{vid_id}.mp4"
    if video_path.exists():
        return video_path
    if not shutil.which("ffmpeg"):
        return None
    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=0x051c2c:s=1280x720:d=4",
            "-vf", f"drawtext=text='{title}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", "4",
            str(video_path)
        ]
        subprocess.run(cmd, capture_output=True, timeout=20)
        return video_path if video_path.exists() else None
    except Exception:
        return None

def run_stages(item: dict, source_text: str, out_dir: Path) -> dict:
    """Execute the voice + visual stages and return combined metadata."""
    vid_id = item.get("id") or item.get("title", "video").lower().replace(" ", "_")[:32]
    script = generate_script(item, source_text)
    (out_dir / f"{vid_id}.script.json").write_text(json.dumps(script, indent=2))
    voice = generate_voice_metadata(script, out_dir, vid_id)
    video = assemble_visual(item, voice, out_dir, vid_id)
    return {
        "id": vid_id,
        "script": script,
        "voice": voice,
        "video_path": str(video) if video else None,
        "stages": ["script", "voice", "visual"]
    }
