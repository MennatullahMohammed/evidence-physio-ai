# The structured fields we ask Claude to extract from each paper's abstract.
# Used by Component 6 to validate that Claude's response is complete.

REQUIRED_EXTRACTION_FIELDS = [
    "population",
    "intervention",
    "comparison",
    "outcome",
    "sample_size",
    "study_design",
    "key_findings",
]

EXTRACTION_PROMPT_TEMPLATE = """You are a clinical research assistant. Extract the following structured information from this study abstract.

Title: {title}
Abstract: {abstract}

Respond with ONLY a JSON object (no other text, no markdown formatting) with exactly these keys:
- population: description of the study population
- intervention: the treatment/intervention studied
- comparison: what it was compared against (or "none" if none)
- outcome: the primary outcome measured
- sample_size: the number of participants (as a string, or "not reported")
- study_design: the type of study design
- key_findings: a brief summary of the main findings

Return ONLY the JSON object, nothing else."""