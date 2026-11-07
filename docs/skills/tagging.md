# Tagging & Metadata Skill

Guidance for producing consistent, searchable tags and machine-readable metadata for every generated video.

## Principles

- **Hybrid tags**: Combine AI-generated concept tags with optional human curation.
- **Provenance first**: Every metadata record must include source URL/commit, generation timestamp, prompts/settings used, and voice/visual style.
- **Searchable**: Tags should support filtering by domain (healthcare, engineering), type (overview, technical, business), and key concepts.
- **Linkable**: Include key timestamps, related source sections, and concept links when relevant.

## Required Metadata Fields (JSON)

- video_id, title, type, duration_seconds
- source: {description, url, commit}
- files: {video, audio, timestamps, script}
- tags: []
- description (short)
- key_concepts: []
- transcript: [{time, text}]
- provenance: {generated_at, generator, voice, visual_style}

## Implementation Notes

- Generate tags from source summary + script.
- Store alongside the MP4.
- Platform loads these records for search, filtering, and grounded chat.
