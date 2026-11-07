# Grok Integration Points

Notes on integrating Grok for grounded chat over generated videos.

## Grounded Chat (preferred)

- Input: user question + selected video transcript + source metadata.
- Behavior: Search transcript first; cite timestamps; only fall back to external knowledge when clearly labeled.
- Implementation options:
  - Client-side keyword search (current React platform).
  - Server-side: send transcript + question to Grok with system prompt enforcing “cite only from transcript unless explicitly external.”
- Distinction: Always prefix responses with “Grounded in this video” or “External exploration”.

## Concept Exploration

- When user asks for broader context, allow web search or Grok general knowledge, but mark it separately.
- Link related source sections or other videos in the harness.

## Platform Integration

- Chat sidebar in the React mini-YouTube.
- Optional: embed Grok API call behind a backend that has access to the full transcript store.
- Keep local transcript as the source of truth.

No live Grok calls are made by default; credentials stay user-side.
