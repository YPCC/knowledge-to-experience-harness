# Step-by-Step Guide: Multi-Source Example with SemRep

This guide shows how the Knowledge-to-Experience Harness handles a combination of heterogeneous inputs (web page, GitHub repository, knowledge-graph registry entry, research paper, and a PowerPoint) and turns them into short educational videos.

**Example topic**: SemRep / Semantic Knowledge Representation Project (NLM) and related modern work on text mining + knowledge graphs for biopharmaceutical process optimization.

## Sources Used

1. LHNCBC project page: Semantic Knowledge Representation Project
2. GitHub repository: https://github.com/lhncbc/SemRep (archived)
3. KG-Hub registry entry: https://kghub.org/kg-registry/resource/semrep/semrep.html
4. Research paper: Integrating text mining and knowledge graph to enhance biopharmaceutical process optimization (PLOS ONE, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0339197)
5. Curated PowerPoint summary created as an additional structured input (`examples/semrep_multisource_example.pptx`)

## Step-by-Step Process

### Step 1: Collect and Summarize Inputs

- Browse / extract key facts from each source (project goals, SemRep pipeline, SemMedDB scale, applications, modern extensions).
- Produce a concise source summary and list of candidate video topics.
- Result: candidate plan saved at `docs/sources/semrep-multisource-plan.md`.

### Step 2: Create an Additional Structured Input (PPTX)

- Build a short PowerPoint that consolidates the multi-source findings into clear slides (sources list, business value, technical pipeline).
- This PPTX becomes one more artifact the harness can ingest (via `scripts/ingest_stub.py` or direct agent processing).

### Step 3: Generate Candidate Video Plan

From the combined summary, select two focused videos:

| Video | Type | Target Length | Audience Focus |
|-------|------|---------------|----------------|
| SemRep for Business: From Literature to Decisions | Business Overview | ≤ 60 s | Pharma, payers, research leaders |
| SemRep Technical Deep Dive | Technical | 60–90 s | NLP / KG practitioners |

### Step 4: Write Scripts

- Business script emphasizes outcomes: literature-based discovery, drug repurposing, clinical guideline support, reusable knowledge assets.
- Technical script explains the pipeline: MetaMap → UMLS concepts → Semantic Network + rules → subject-relation-object triples → SemMedDB, and links to modern text-mining + KG frameworks.

### Step 5: Generate Narration

- Use a clear professional voice (e.g., Orion / Atlas).
- Produce MP3 + timestamp JSON for each script.

### Step 6: Create Visuals and Assemble Videos

- Generate clean educational slides matching the visual-style skill.
- Assemble each video with ffmpeg (static slide + narration, web-compatible MP4).
- Outputs:
  - `semrep_business_overview_v1.mp4` (~53 s)
  - `semrep_technical_deepdive_v1.mp4` (~63 s)

### Step 7: Metadata and Provenance

- Record short description, tags, source URLs, key timestamps, and transcript snippets.
- Log the run in `docs/generation-log.md`.
- Optionally register entries in `platform/public/videos.json` for the mini-platform.

## How to Repeat This Pattern

1. Gather any mix of sources (GitHub URL, paper, web page, existing PPTX/PDF, video).
2. Produce a short candidate plan (see existing plans in `docs/sources/`).
3. Follow skill documents in `docs/skills/` for voice and visual style.
4. Generate narration + visuals → assemble MP4s + transcripts + metadata.
5. Update the consumption platform or embed the videos.

The same modular stages work for any domain. SemRep is simply one concrete multi-source demonstration.

## Related Files

- Candidate plan: [docs/sources/semrep-multisource-plan.md](sources/semrep-multisource-plan.md)
- Quick Start: [docs/quick-start.md](quick-start.md)
- Ingestion path: [docs/ingestion-path.md](ingestion-path.md)
- LLM configuration: [docs/llm-configuration.md](llm-configuration.md)

**Knowledge in. Trusted experiences out.**
