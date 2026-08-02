import json

from app.services.claude_extraction_service import ClaudeExtractionService
from data.extraction_schema import REQUIRED_EXTRACTION_FIELDS


class ClaudeEvidenceExtractionEngine:
    """
    Component 6 — Claude Evidence Extraction Engine

    Responsibilities:
    1. Process each paper one at a time (sequential, per AD-003)
    2. Call Claude to extract structured data from the paper's abstract
    3. Validate the response against the required schema (per AD-004)
    4. Retry on failure; skip and log the paper if retries are exhausted
       (per AD-005), without stopping the whole pipeline
    5. Cache validated results in memory so a paper isn't re-extracted
       within the same run (per AD-006)
    """

    MAX_RETRIES = 2

    def __init__(self):
        self.service = ClaudeExtractionService()
        self.cache = {}         # temporary in-memory storage, keyed by PMID
        self.error_log = []     # records of papers that failed after retries

    def extract_single_paper(self, paper):
        """
        Step 2-4 (for one paper): call Claude, parse the JSON response,
        validate it, and retry on failure up to MAX_RETRIES times.
        Returns the validated dict, or None if extraction ultimately failed.
        """
        pmid = paper.get("pmid")

        # Step 5: skip re-extraction if this paper was already processed
        if pmid in self.cache:
            return self.cache[pmid]

        last_error = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                raw_response = self.service.extract(
                    title=paper.get("title"),
                    abstract=paper.get("abstract"),
                )
                parsed = json.loads(raw_response)

                if self._is_valid(parsed):
                    self.cache[pmid] = parsed
                    return parsed

                last_error = "Response failed schema validation"

            except json.JSONDecodeError:
                last_error = "Response was not valid JSON"
            except Exception as e:
                last_error = str(e)

        # All retries exhausted — log and move on (AD-005)
        self.error_log.append({
            "pmid": pmid,
            "reason": last_error,
            "retry_count": self.MAX_RETRIES,
        })
        return None

    def _is_valid(self, parsed_response):
        """
        Checks that the parsed response has all required fields.
        """
        if not isinstance(parsed_response, dict):
            return False

        for field_name in REQUIRED_EXTRACTION_FIELDS:
            if field_name not in parsed_response:
                return False

        return True

    def process(self, prioritized_evidence):
        """
        Step 1: Loop through papers one at a time (sequential processing).
        Returns a dict with the validated structured evidence and the
        error log for any papers that failed.
        """
        self.validated_evidence = []

        for paper in prioritized_evidence:
            result = self.extract_single_paper(paper)
            if result is not None:
                # Keep the original paper metadata alongside the extraction
                combined = dict(paper)
                combined["extracted_data"] = result
                self.validated_evidence.append(combined)

        return {
            "validated_evidence": self.validated_evidence,
            "error_log": self.error_log,
        }



if __name__ == "__main__":
    # A single sample paper — we keep this small since it makes a
    # real, billable call to the Claude API.
    sample_paper = {
        "pmid": "9999999",
        "title": "Effectiveness of eccentric exercise for rotator cuff tendinopathy",
        "abstract": (
            "This randomized controlled trial evaluated 60 adults with "
            "chronic rotator cuff tendinopathy. Participants were assigned "
            "to either a 12-week eccentric exercise program or standard "
            "physiotherapy care. The exercise group showed significantly "
            "greater improvement in shoulder pain and function scores at "
            "12 weeks compared to the control group (p < 0.05)."
        ),
        "publication_type": "randomized controlled trial",
        "publication_year": "2022",
    }

    engine = ClaudeEvidenceExtractionEngine()
    result = engine.process([sample_paper])

    print("Component 6 ran successfully!")
    print("Number of validated papers:", len(result["validated_evidence"]))
    print("Number of failed papers:", len(result["error_log"]))

    if result["validated_evidence"]:
        extracted = result["validated_evidence"][0]["extracted_data"]
        print("\nExtracted data:")
        for key, value in extracted.items():
            print(f"  {key}: {value}")

    if result["error_log"]:
        print("\nErrors:")
        for error in result["error_log"]:
            print(f"  {error}")