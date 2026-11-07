# Voice Skill — Multi-Speaker Narration

Reusable guidance for consistent, clear voice generation in Knowledge-to-Experience videos.

## Principles

- **Clarity first**: Neutral, professional pace. Avoid heavy accent or extreme expressiveness unless the content demands it.
- **Match the content**: Technical deep-dives use steady, authoritative voices. Business explainers can be slightly warmer.
- **Multi-speaker when useful**: Use different voices for dialogue-style or contrasting viewpoints (e.g., “business” vs “technical”).
- **Consistent casting**: Prefer the same voice across a video series for brand continuity (e.g., Orion for primary technical narration).
- **Timestamps**: Always generate with character-level or word-level timestamps for transcript alignment.

## Available Voices (examples)

- Orion / Atlas / Helios — clear male technical
- Ara / Aurora / Celeste — clear female professional
- Use multi-speaker tool for dialogue turns with controlled gaps.

## Implementation Notes

- Primary tool: Voice generate_speech / generate_multi_speech.
- Output: MP3 + timestamps JSON.
- Keep intermediate audio for re-assembly or captioning.
- Language hint: “en” or “auto”.

This skill can be swapped for different TTS providers while keeping the same prompt and casting conventions.
