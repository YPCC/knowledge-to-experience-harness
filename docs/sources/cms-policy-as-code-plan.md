# Candidate Video Plan — cms-policy-as-code

**Source**: https://github.com/YPCC/cms-policy-as-code  
**Commit / SHA**: b548f6d07817acd7f3d8acd4b75f1307926a413d  
**Date**: 2026-11-06  
**Domain**: Healthcare — CMS Policy-as-Code / Context Graph Engine

## Source Summary

Neuro-Symbolic system that converts unstructured CMS NCD/LCD policies into executable, auditable coverage rules. Uses LLM-assisted extraction into a versioned Neo4j Context Graph, then deterministic rules engine at runtime that produces full Decision Traces. Grounded to official coding systems. Addresses payer pain of inconsistent manual interpretation, hallucination risk, and brittle pure-rules systems.

## Candidate Videos

| # | Title | Type | Length | Focus | Business / Technical |
|---|-------|------|--------|-------|-----------------------|
| 1 | CMS Policy-as-Code: From Unstructured Documents to Auditable Rules | Overview | 60–90s | High-level problem, solution, value | Business + Technical |
| 2 | Why Policy-as-Code Matters for Healthcare Payers | Business explainer | 60–90s | Pain points (delays, denials, compliance), benefits | Business |
| 3 | Neuro-Symbolic Architecture Explained | Technical deep-dive | 90–120s | Extraction → Graph → Deterministic Rules → Decision Trace | Technical |
| 4 | How a Claim Becomes a Decision Trace | How-it-works | 90s | End-to-end flow on Vitamin D example | Technical |
| 5 | Context Graph, Grounding & Provenance | Short explainer | 60s | Versioning, official coding systems, citations | Technical |
| 6 | Spec-Kit Agents and Governance | Dialogue / overview | 60s | Multi-agent development approach | Technical |

## Key Concepts to Cover

- Neuro-Symbolic design (LLM for extraction only; deterministic at runtime)
- Context Graph (Neo4j, versioned, provenanced)
- Decision Trace (immutable, auditable)
- Grounding to ICD-10-CM, CPT, HCPCS, SNOMED CT
- Provenance-first and human review gates
- Spec-Kit driven agent development

## Next Generation Steps

1. Produce scripts for videos 1 and 2.
2. Generate narration + simple visual assembly (or Manim where valuable).
3. Create metadata JSON + tags for each.
4. Ingest into the mini-YouTube React platform.

**Note**: System is designed to be generic — same pipeline works for PowerPoint, PDFs, papers, or any other source material.
