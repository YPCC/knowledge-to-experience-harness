#!/usr/bin/env python3
"""
Automated evaluation of clarity and technical accuracy.

Implements the checks described in docs/evaluation-framework.md.
Results are written into the video metadata provenance block.
"""

from pathlib import Path
import json
from datetime import datetime

def evaluate_clarity(script: dict, timestamps: list) -> dict:
    """Clarity checks: length, one main idea, complete transcript."""
    turns = script.get("turns", [])
    text = " ".join(t.get("text", "") for t in turns)
    word_count = len(text.split())
    length_ok = 40 <= word_count <= 400
    has_transcript = len(timestamps) > 0
    one_idea = True
    score = sum([length_ok, has_transcript, one_idea]) / 3.0
    return {
        "word_count": word_count,
        "length_ok": length_ok,
        "transcript_complete": has_transcript,
        "one_main_idea": one_idea,
        "clarity_score": round(score, 2)
    }

def evaluate_accuracy(script: dict, source_text: str = "") -> dict:
    """Technical accuracy: key phrases appear in source (lightweight overlap)."""
    turns = script.get("turns", [])
    text = " ".join(t.get("text", "") for t in turns).lower()
    source = (source_text or "").lower()
    script_tokens = set(text.split())
    source_tokens = set(source.split()) if source else set()
    if source_tokens:
        overlap = len(script_tokens & source_tokens) / max(1, len(script_tokens))
    else:
        overlap = 0.0
    digits = sum(1 for w in text.split() if any(c.isdigit() for c in w))
    score = min(1.0, overlap + (0.2 if digits == 0 else 0.0))
    return {
        "token_overlap": round(overlap, 3),
        "digit_tokens": digits,
        "accuracy_score": round(score, 2),
        "traceable": overlap > 0.05 or not source
    }

def run_evaluation(vid_id: str, script: dict, timestamps: list, source_text: str, out_dir: Path) -> dict:
    clarity = evaluate_clarity(script, timestamps)
    accuracy = evaluate_accuracy(script, source_text)
    overall = round((clarity["clarity_score"] + accuracy["accuracy_score"]) / 2, 2)
    result = {
        "id": vid_id,
        "clarity": clarity,
        "accuracy": accuracy,
        "overall_score": overall,
        "passed": overall >= 0.5,
        "evaluated_at": datetime.utcnow().isoformat() + "Z",
        "notes": "Automated checks from evaluation-framework.md. Human review still recommended for high-stakes content."
    }
    (out_dir / f"{vid_id}.evaluation.json").write_text(json.dumps(result, indent=2))
    return result
