# EvidencePhysio AI

An AI-powered Clinical Decision Support System (CDSS) that helps physiotherapists find, evaluate, and summarize evidence-based treatment evidence after a working diagnosis has already been established.

EvidencePhysio AI does **not** perform diagnosis, differential diagnosis, clinical reasoning, or medical decision-making. It retrieves, evaluates, synthesizes, and explains published scientific evidence to support treatment planning. The physiotherapist stays in control of the final decision.

## Overview

Given a patient's clinical profile (working diagnosis, symptoms, functional limitations, goals, etc.), the system:

1. Validates and structures the patient's clinical information
2. Identifies missing clinical information relevant to the diagnosis
3. Builds an optimized PubMed search query
4. Retrieves relevant, recent research from PubMed
5. Prioritizes the most relevant and highest-quality studies (rule-based)
6. Extracts structured clinical findings from each study using Claude
7. Scores the overall confidence of the evidence (rule-based)
8. Synthesizes a patient-specific summary of the findings
9. Explains the evidence and its limitations in plain language
10. Generates a final report (human-readable and machine-readable JSON)

## Architecture

The system is a 10-component sequential pipeline. Design choices:
- Single Responsibility Principle: one job per component
- Rule-based, deterministic logic wherever possible (search scoring, evidence prioritization, confidence rating)
- Claude (Anthropic API) used only where natural language understanding or generation is actually needed: evidence extraction, synthesis, explanation
- Human-in-the-loop checkpoints for decisions like expanding a search that returned too few results
- A single failed study does not stop the pipeline

Full architecture details are in [`docs/04_Architecture.md`](docs/04_Architecture.md).

## Pipeline Components

| # | Component | Uses Claude API? |
|---|---|---|
| 1 | Patient Information Manager | No |
| 2 | Missing Clinical Information Engine | No |
| 3 | Search Strategy Builder | No |
| 4 | PubMed Retrieval Engine | No |
| 5 | Evidence Prioritization Engine | No |
| 6 | Claude Evidence Extraction Engine | Yes |
| 7 | Evidence Confidence Engine | No |
| 8 | Evidence Synthesis Engine | Yes |
| 9 | Natural Language Explanation Engine | Yes |
| 10 | Evidence Report Generator | No |

## Tech Stack

- **Language:** Python 3.10
- **AI:** Anthropic Claude API (evidence extraction, synthesis, explanation)
- **Data source:** NCBI PubMed E-utilities API
- **Key libraries:** `requests`, `anthropic`, `python-dotenv`

## Project Structure
```
evidence-physio-ai/
├── app/
│ ├── components/ # The 10 pipeline components
│ ├── models/ # Patient data model
│ ├── services/ # External API communication (PubMed, Claude)
│ └── utils/
├── data/ # Diagnosis knowledge base, scoring/search rules, prompt templates
├── docs/ # Architecture and design documentation
├── tests/ # (in progress)
├── main.py # Runs the full end-to-end pipeline
└── requirements.txt
```

## Running the Pipeline

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with:
```
ANTHROPIC_API_KEY=your_key_here
```

Run the full pipeline (uses a sample patient):
```bash
python -m main
```

Each component can also be run individually for testing:
```bash
python -m app.components.patient_information_manager
```

## Status

**Work in progress, MVP stage.**

- All 10 components implemented
- Components 1, 2, 3, 4, 5, 7, and 10 fully verified
- Components 6, 8, and 9 (Claude-dependent) implemented but pending final verification (API credit)
- Unit test suite in progress

## About This Project

This project is a learning exercise in software architecture and Python, built alongside a real portfolio piece. The emphasis is on clean, modular, single-responsibility design over speed of implementation.