# Candidate Video Plan — SemRep Multi-Source Example

**Sources combined**:
- LHNCBC Semantic Knowledge Representation Project page
- GitHub: https://github.com/lhncbc/SemRep (archived)
- KG-Hub registry: https://kghub.org/kg-registry/resource/semrep/semrep.html
- PLOS ONE paper: Integrating text mining and knowledge graph to enhance biopharmaceutical process optimization (10.1371/journal.pone.0339197)
- Curated PowerPoint: `examples/semrep_multisource_example.pptx` (created as an additional input)

**Date**: 2026-11-17
**Domain**: Biomedical NLP / Knowledge Graphs / Literature-based Discovery

## Source Summary

SemRep (NLM) extracts semantic predications (subject-relation-object triples) from biomedical free text using MetaMap + UMLS Metathesaurus and Semantic Network. Output powers SemMedDB, a PubMed-scale knowledge resource widely used for literature-based discovery, drug repurposing, clinical guideline support, and hypothesis generation. The modern PLOS ONE work shows the same pattern applied to biopharmaceutical process optimization (text mining → ontology → knowledge graph).

This example demonstrates the harness ingesting heterogeneous inputs (web page, GitHub repo, registry entry, research paper, and a PPTX summary) and producing focused short videos.

## Candidate Videos

| # | Title | Type | Target Length | Focus | Status |
|---|-------|------|---------------|-------|--------|
| 1 | SemRep for Business: From Literature to Decisions | Business Overview | ≤ 60s | Value for pharma, payers, research orgs | Generated |
| 2 | SemRep Technical Deep Dive | Technical | 60–90s | MetaMap + Semantic Network → triples → SemMedDB; link to modern KG frameworks | Generated |

## Key Concepts Covered

- Semantic predications / subject-relation-object triples
- UMLS grounding (Metathesaurus + Semantic Network)
- SemMedDB as literature-scale knowledge base
- Applications: literature-based discovery, drug repurposing, clinical guidelines
- Continuity with contemporary text-mining + KG systems

## Artifacts Produced

- `videos/semrep_business_overview_v1.mp4` (~53s)
- `videos/semrep_technical_deepdive_v1.mp4` (~63s)
- Matching narrations + timestamps
- `examples/semrep_multisource_example.pptx`
- Metadata entries (see platform/public/videos.json or companion JSON)

**Note**: This is the multi-source example for the harness. The same pipeline works for any combination of GitHub, documents, papers, slides, or web content.
