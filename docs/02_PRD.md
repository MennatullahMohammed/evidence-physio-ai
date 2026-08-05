# EvidencePhysio AI — Product Requirements Document (PRD)

## Overview

EvidencePhysio AI is a clinical decision support tool that retrieves, evaluates, and summarizes published evidence relevant to a physiotherapy patient's working diagnosis. It doesn't diagnose, and it doesn't choose a treatment on the clinician's behalf. See `01_Product_Vision.md` for the reasoning behind the product; this document defines what the system needs to do.

## Goals

- Let a physiotherapist enter a patient's clinical profile and get a relevant, evidence-based summary in under a minute
- Base every claim in the output on real, citable, recent literature
- Make the system's confidence in its own output explicit and honest, rather than presenting all evidence as equally reliable
- Keep a human physiotherapist in control of the final clinical decision at every step

## Non-Goals

- Diagnosing a patient or suggesting a working diagnosis
- Recommending a specific treatment as the "correct" choice
- Replacing a physiotherapist's clinical judgment
- Storing or managing patient records long-term (this is a single-session evidence lookup tool, not an EHR)

## Users

- **Primary:** licensed physiotherapists using the tool during treatment planning
- **Secondary:** physiotherapy students checking what the literature says for a case they're studying

## Functional Requirements

### Input
The system must accept a patient's clinical profile: working diagnosis, age, sex, symptom duration, pain severity (0-10 NRS), functional limitations, previous treatments, and diagnosis-specific fields (occupation, activity level, dominant side, etc., depending on the diagnosis).

### Missing information handling
If information relevant to the diagnosis is missing from the patient profile, the system must identify what's missing and let the physiotherapist decide whether to add it or proceed without it. It must not silently guess missing clinical details.

### Evidence retrieval
The system must build a search query from the patient's diagnosis and search terms, and retrieve matching studies from PubMed. If a search returns zero or very few results, the system must flag this and offer to broaden the search, with the physiotherapist's approval required before doing so.

### Evidence prioritization
Retrieved studies must be deduplicated and ranked by a transparent, rule-based relevance score (study type, recency, sample size, and similar factors), not by opaque or AI-driven ranking.

### Evidence extraction
For each prioritized study, the system must extract structured clinical information (population, intervention, comparison, outcome, sample size, study design, key findings) from the abstract. A failure on one study must not stop processing of the others.

### Confidence rating
The system must produce an overall confidence rating (High / Moderate / Low / Very Low) for the evidence set, using fixed, explainable rules (see `06_Confidence_Rules.md`), along with a plain-language explanation of the rating.

### Synthesis and explanation
The system must produce a short, patient-specific summary of what the evidence means for this particular patient, and a natural-language explanation of the confidence rating and its limitations, written for a physiotherapist rather than a researcher.

### Final report
The system must generate a complete report combining all of the above: patient summary, search strategy, selected studies, confidence rating, patient-specific summary, explanation, and full references, available in both a human-readable form and a structured (JSON) form.

## Non-Functional Requirements

- **Explainability:** every score, ranking, and confidence rating must be traceable to a specific rule, not a black-box decision
- **Fault tolerance:** a failure processing one study (API error, malformed data) must not stop the rest of the pipeline
- **Human-in-the-loop:** any decision to broaden a search beyond what the physiotherapist originally specified requires explicit confirmation
- **Data honesty:** the system must not present fabricated or hallucinated findings as if they came from a real study

## Out of Scope (for now)

- Multi-patient case management or history
- Integration with an EHR or hospital system
- Support for diagnoses outside the current Diagnosis Knowledge Base (expandable over time, not exhaustive at launch)
- Mobile app (current interface is a web-based Streamlit app)

## Success Criteria for the MVP

- A physiotherapist can complete the full flow (enter patient data, get a report) without errors, for at least one supported diagnosis
- The evidence returned is real and traceable to actual PubMed records, not fabricated
- The confidence rating changes appropriately based on the quality and quantity of evidence found, rather than staying fixed or meaningless
- The system falls back to a demo case correctly when PubMed search doesn't return usable results, rather than failing silently