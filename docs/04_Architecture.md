# EvidencePhysio AI — System Architecture (v1)

**Version:** 1.0 (Draft)

## Overview

EvidencePhysio AI is an AI-powered Clinical Decision Support System (CDSS) that helps physiotherapists find, evaluate, and summarize evidence-based treatment evidence after a working diagnosis has already been established.

The system does **not** perform diagnosis, differential diagnosis, clinical reasoning, or medical decision-making. It retrieves, evaluates, synthesizes, and explains published scientific evidence to support treatment planning.

## Design Principles

- Modular architecture with single responsibility per component
- Separation of concerns
- Deterministic, rule-based decision-making wherever possible
- Human-in-the-loop for critical situations
- Fault-tolerant processing pipeline
- Explainable, reproducible results
- Scalable component design

## Diagnosis Knowledge Base

A structured resource used by the Search Strategy Builder. Each diagnosis entry contains a diagnosis name, medical keywords, synonyms, MeSH terms, search-relevant fields, and personalization fields. The Search Strategy Builder reads this knowledge base directly rather than asking an LLM to determine search terms, which keeps search-term selection deterministic, fast, and easy to maintain and extend.

## High-Level Architecture

```
Patient Information
        │
        ▼
Patient Information Manager
        │
        ▼
Missing Clinical Information Engine
        │
        ▼
Search Strategy Builder
        │
        ▼
PubMed Retrieval Engine
        │
        ▼
Evidence Prioritization Engine
        │
        ▼
Claude Evidence Extraction Engine
        │
        ▼
Evidence Confidence Engine
        │
        ▼
Evidence Synthesis Engine
        │
        ▼
Natural Language Explanation Engine
        │
        ▼
Evidence Report Generator
```

## Architecture Decisions

**AD-001 — Human-in-the-Loop.** If PubMed returns no relevant studies, or too few, the system detects the shortfall, suggests a search expansion, and waits for the physiotherapist to confirm before running the broader search. Search expansion always stays under clinician supervision.

**AD-002 — Rule-Based Evidence Confidence.** Evidence confidence is calculated using predefined rule-based criteria; no LLM participates in confidence scoring. This keeps the scoring explainable, deterministic, reproducible, and easy to validate.

**AD-003 — Sequential Processing.** Papers are processed one at a time, which simplifies debugging, retry handling, and fault tolerance, and limits the impact of any single API failure.

**AD-004 — JSON Validation.** Every Claude response must pass schema validation before entering the pipeline; invalid outputs are rejected automatically.

**AD-005 — Fault Tolerance.** A single paper failing must never stop the pipeline — the system skips it after retry attempts and continues with the rest.

**AD-006 — Data Persistence.** Validated structured evidence is stored temporarily before downstream processing, so it isn't re-extracted during the same run.

---

## Component 1 — Patient Information Manager

Collects, validates, and organizes patient information before it enters the pipeline.

**Input:** Patient information from the user interface — working diagnosis, age, sex, symptom duration, pain severity, functional limitations, previous treatments, clinical notes, and any diagnosis-specific fields the system requires.

**Processing:** Collects the data, validates required fields and input format/type, normalizes it, and builds a standardized Patient Profile.

**Output:** A validated Patient Profile.

**Next:** Missing Clinical Information Engine

---

## Component 2 — Missing Clinical Information Engine

Identifies missing clinical information before the search strategy is built.

**Input:** Patient Profile and a diagnosis-specific clinical checklist.

**Processing:** Compares the profile against the checklist, detects missing fields, and presents them to the physiotherapist, who decides whether to fill them in or continue without them.

**Output:** Complete Patient Context (if information is added) or Patient Context (Incomplete) (if the physiotherapist proceeds without it).

**Next:** Search Strategy Builder

---

## Component 3 — Search Strategy Builder

Builds an optimized PubMed search query from the patient's clinical information.

**Input:** Patient Context, the Diagnosis Knowledge Base, and search rules.

**Processing:** Reads the diagnosis from the Patient Context, loads the matching Diagnosis Knowledge Base entry, pulls its medical keywords, synonyms, MeSH terms, search-relevant fields, and personalization fields, and combines these with the patient context and search rules to construct the query.

**Output:** Optimized PubMed search query.

**Next:** PubMed Retrieval Engine

---

## Component 4 — PubMed Retrieval Engine

Retrieves relevant publications from PubMed.

**Input:** Optimized PubMed search query.

**Processing:** Submits the query, retrieves matching publications, extracts article metadata (PMID, title, authors, journal, publication year, abstract, DOI, publication type), and checks the number of results returned.

**Edge case — zero results:** Activates the human-in-the-loop workflow: suggests expanding the search, asks the physiotherapist whether to retry with broader criteria, and if approved, generates an expanded query and repeats the search.

**Output:** Retrieved evidence metadata.

**Next:** Evidence Prioritization Engine

---

## Component 5 — Evidence Prioritization Engine

Prioritizes retrieved studies and selects the most relevant, highest-quality evidence.

**Processing:** Removes duplicates, calculates a rule-based relevance score for each study, ranks studies by that score, and selects the top evidence. If the available evidence is limited, it notifies the user and offers search-expansion options.

Internal modules: deduplication, ranking engine, relevance scoring, top-evidence selection.

Relevance is scored on study type, publication year, sample size, population match, intervention match, and outcome match — all rule-based; no AI model is involved in prioritization.

**Output:** Prioritized evidence set.

**Next:** Claude Evidence Extraction Engine

---

## Component 6 — Claude Evidence Extraction Engine

Extracts structured clinical information from each prioritized paper.

**Input:** Prioritized evidence set.

**Processing:** Each paper moves through the same pipeline independently — Claude extraction → structured JSON → schema validation → validated JSON → temporary RAM storage — one paper at a time, for easier debugging and lower impact from any single API failure.

Every Claude response is checked against the schema for required fields, correct data types, valid JSON, and missing values; only validated JSON continues downstream.

If extraction or validation fails, the engine retries automatically up to a limited number of times. If retries still fail, it logs the error (paper identifier, failure reason, retry count, timestamp) and moves on — one failed paper never stops the pipeline. Validated JSON is held temporarily in RAM so a paper isn't re-extracted within the same run.

**Output:** Validated structured evidence set.

**Next:** Evidence Confidence Engine

---

## Component 7 — Evidence Confidence Engine

Evaluates the overall strength and reliability of the available evidence.

**Input:** Validated structured evidence set.

**Processing:** Evaluates individual study quality, compares quality across studies, and applies predefined confidence rules to classify the overall evidence as High, Moderate, Low, or Very Low, with an explanation for the rating. Like the prioritization engine, this is rule-based rather than LLM-scored, for explainability and reproducibility.

**Output:** Overall evidence confidence.

**Next:** Evidence Synthesis Engine

---

## Component 8 — Evidence Synthesis Engine

Combines the evidence with the patient's clinical context to produce a personalized summary — personalizing the *interpretation* of the evidence, not the evidence itself.

**Input:** Validated structured evidence set, patient clinical context, overall evidence confidence.

**Processing:** Analyzes the evidence against the patient's context, identifies the findings most clinically relevant to this patient, and generates a patient-specific summary.

**Output:** Patient-specific evidence summary.

**Next:** Natural Language Explanation Engine

---

## Component 9 — Natural Language Explanation Engine

Converts the evidence analysis into a clear explanation for the physiotherapist — explaining the outputs of earlier components rather than generating new evidence or recommendations.

**Input:** Patient-specific evidence summary, overall evidence confidence.

**Processing:** Translates the structured evidence into natural language, explains the confidence level, and highlights important limitations and uncertainties in clinician-friendly language.

**Output:** Natural language evidence explanation.

**Next:** Evidence Report Generator

---

## Component 10 — Evidence Report Generator

Produces the final report presented to the physiotherapist.

**Input:** Patient profile, optimized PubMed search query, prioritized evidence set, validated structured evidence, overall evidence confidence, patient-specific evidence summary, natural language explanation.

**Processing:** Assembles all of the above into a structured report with attached references.

**Output:**
1. Final evidence-based clinical report (human-readable)
2. Structured report (machine-readable JSON)

Sections: patient summary, search strategy, selected studies, evidence confidence, patient-specific evidence summary, natural language explanation, references.

---

## Architecture Status

Version 1.0 (Draft) — architecture, components, processing pipeline, and major architectural decisions are complete. Next step: begin implementation.