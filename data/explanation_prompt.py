# Prompt template used by Component 9 to ask Claude to translate the
# patient-specific evidence summary into a clear, clinician-friendly
# explanation.

EXPLANATION_PROMPT_TEMPLATE = """You are helping a physiotherapist understand a piece of clinical evidence analysis.

Patient-specific evidence summary:
{patient_specific_summary}

Overall evidence confidence: {confidence_level}
Confidence explanation: {confidence_explanation}

Write a clear, natural-language explanation (4-6 sentences) for the physiotherapist that:
- Explains what the evidence summary means in plain language
- Explains what the confidence level means and why it matters for decision-making
- Highlights any important limitations or uncertainties the physiotherapist should keep in mind
- Does NOT introduce new clinical claims beyond what's already stated above

Respond with ONLY the explanation text, no headers, no markdown."""