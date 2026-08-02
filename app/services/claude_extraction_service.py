import os
from anthropic import Anthropic
from dotenv import load_dotenv

from data.extraction_schema import EXTRACTION_PROMPT_TEMPLATE

load_dotenv()  # reads the .env file and loads ANTHROPIC_API_KEY into the environment


class ClaudeExtractionService:
    """
    Handles raw communication with the Claude API.
    This is the only place in the codebase that talks directly to Claude
    for evidence extraction.
    """

    MODEL_NAME = "claude-sonnet-5"

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Make sure it's set in your .env file."
            )
        self.client = Anthropic(api_key=api_key)

    def extract(self, title, abstract):
        """
        Send a paper's title and abstract to Claude, and return the
        raw text response (expected to be a JSON string).
        """
        prompt = EXTRACTION_PROMPT_TEMPLATE.format(
            title=title or "Not available",
            abstract=abstract or "Not available",
        )

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text