# Evaluation Framework — Clarity & Technical Accuracy

Lightweight checks for every generated video before it is considered “trusted.”

## Clarity Checks

- Script length matches target (60–120s).
- One main idea per video; progressive disclosure.
- Visuals support (do not contradict) the narration.
- On-screen text is sparse and high-contrast.
- Transcript is complete and timestamped.

## Technical Accuracy Checks

- Claims traceable to the source (GitHub commit, paper section, document span).
- No invented numbers, APIs, or results.
- Grounding statements (coding systems, versions, architecture) match source.
- Decision traces / provenance claims are accurate.

## Process

1. Automated: Compare key phrases in script against extracted source text.
2. Human review gate (optional but recommended for high-stakes domains).
3. Record evaluation result in the metadata provenance block.
4. Flag videos that fail for regeneration.

This framework is modular and can be extended with automated scoring or SME review workflows.
