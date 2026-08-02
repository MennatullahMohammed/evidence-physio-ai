import os
from anthropic import Anthropic
from dotenv import load_dotenv

from data.explanation_prompt import EXPLANATION_PROMPT_TEMPLATE

load_dotenv()


class ClaudeExplanationService:
    """
    Handles raw communication with the Claude API for natural language
    explanation generation. This is the only place in the codebase
    that talks directly to Claude for this purpose.
    """

    MODEL_NAME = "claude-sonnet-5"

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Make sure it's set in your .env file."
            )
        self.client = Anthropic(api_key=api_key)

    def explain(self, patient_specific_summary, confidence_level, confidence_explanation):
        prompt = EXPLANATION_PROMPT_TEMPLATE.format(
            patient_specific_summary=patient_specific_summary,
            confidence_level=confidence_level,
            confidence_explanation=confidence_explanation,
        )

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text