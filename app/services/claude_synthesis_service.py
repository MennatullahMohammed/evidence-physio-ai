import os
from anthropic import Anthropic
from dotenv import load_dotenv

from data.synthesis_prompt import SYNTHESIS_PROMPT_TEMPLATE

load_dotenv()


class ClaudeSynthesisService:
    """
    Handles raw communication with the Claude API for evidence synthesis.
    This is the only place in the codebase that talks directly to Claude
    for this purpose.
    """

    MODEL_NAME = "claude-sonnet-5"

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Make sure it's set in your .env file."
            )
        self.client = Anthropic(api_key=api_key)

    def synthesize(self, patient, confidence_level, evidence_summaries):
        prompt = SYNTHESIS_PROMPT_TEMPLATE.format(
            working_diagnosis=patient.working_diagnosis,
            age=patient.age,
            pain_severity=patient.pain_severity,
            functional_limitations=", ".join(patient.functional_limitations) or "none reported",
            patient_goals=", ".join(patient.patient_goals) or "none reported",
            confidence_level=confidence_level,
            evidence_summaries=evidence_summaries,
        )

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text