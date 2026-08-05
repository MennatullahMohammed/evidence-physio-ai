# EvidencePhysio AI — Project Roadmap

## Current Status

All 10 pipeline components are implemented and connected end-to-end, from patient input through to a final report. The system connects to real external data (PubMed) and produces real, structured output rather than placeholder text.

| Component | Status |
|---|---|
| 1. Patient Information Manager | Verified |
| 2. Missing Clinical Information Engine | Verified |
| 3. Search Strategy Builder | Verified (fixed a PubMed date-syntax bug that was silently returning zero results) |
| 4. PubMed Retrieval Engine | Verified (fixed a publication-type extraction bug affecting downstream scoring) |
| 5. Evidence Prioritization Engine | Verified |
| 6. Claude Evidence Extraction Engine | Implemented, pending verification (needs Claude API credit) |
| 7. Evidence Confidence Engine | Verified |
| 8. Evidence Synthesis Engine | Implemented, pending verification (needs Claude API credit) |
| 9. Natural Language Explanation Engine | Implemented, pending verification (needs Claude API credit) |
| 10. Evidence Report Generator | Verified |

A Streamlit web interface sits on top of the pipeline, letting a physiotherapist fill out a patient form and get a generated report directly in the browser.

## Near-Term (next few weeks)

- **Verify Components 6, 8, 9** against the real Claude API once credit is available, replacing the placeholder functions currently used in `main.py` and `streamlit_app.py`
- **Write a unit test suite** (`tests/`) covering validation logic, edge cases (missing fields, zero PubMed results, malformed API responses), and the rule-based scoring in Components 5 and 7
- **Deep-review every component** line by line, until any design decision in the codebase can be explained without checking notes

## Medium-Term

- **Expand the Diagnosis Knowledge Base** beyond the current small set of diagnoses (currently rotator cuff tendinopathy and low back pain), adding checklists and search vocabulary for other common physiotherapy diagnoses
- **Improve the personalization logic in Component 3.** Patient attributes like occupation and activity level are gathered but not currently used to narrow the PubMed search, since including them as mandatory filters was returning zero results. Using them for re-ranking instead of filtering is worth exploring
- **Add persistent error logging** for failed extractions and API calls, beyond the in-memory error log Component 6 keeps during a single run
- **Improve fallback handling** so that when PubMed returns no usable results, the physiotherapist is told clearly they're viewing a demonstration case, with the option to try a broader search themselves

## Longer-Term / Exploratory

- **Validate the confidence-scoring rules** against how experienced physiotherapists actually judge evidence quality, and adjust the point system in `confidence_rules.py` if it doesn't match real clinical judgment
- **Test the tool with real physiotherapists** on real (anonymized) cases, and let that feedback guide what gets built next instead of continuing to guess
- **Consider a proper backend/API layer** if the project grows past a single-session Streamlit tool, for saved cases, user accounts, or integration with other tools
- **Add support for search expansion** as a genuine human-in-the-loop feature. The pipeline already detects low or zero results and flags it, but the "ask the physiotherapist and expand" loop described in the architecture isn't fully wired up yet

## Explicitly Not Planned Right Now

- Diagnosis or treatment recommendation features (out of scope by design, see `01_Product_Vision.md`)
- EHR integration
- Mobile app
- Multi-patient history/records management

This list stays here on purpose: scope is a decision, not something that happens by default.