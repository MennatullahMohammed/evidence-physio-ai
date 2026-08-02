from data.confidence_rules import (
    STUDY_QUALITY_POINTS,
    DEFAULT_QUALITY_POINTS,
    LARGE_SAMPLE_THRESHOLD,
    LARGE_SAMPLE_BONUS,
    CONFIDENCE_THRESHOLDS,
    MIN_STUDIES_FOR_HIGH_CONFIDENCE,
)


class EvidenceConfidenceEngine:
    """
    Component 7 — Evidence Confidence Engine

    Responsibilities:
    1. Evaluate the quality of each individual validated study
    2. Compare quality across all studies (calculate an average score)
    3. Apply predefined rules to classify overall confidence
       (High / Moderate / Low / Very Low)
    4. Provide a plain-language explanation for the rating
    """

    def evaluate_study_quality(self, study):
        """
        Step 1 (per study): Score a single study based on its
        study design and sample size.
        """
        extracted_data = study.get("extracted_data", {})
        study_design = (extracted_data.get("study_design") or "").strip().lower()

        design_score = STUDY_QUALITY_POINTS.get(study_design, DEFAULT_QUALITY_POINTS)

        sample_bonus = self._calculate_sample_bonus(extracted_data.get("sample_size"))

        return design_score + sample_bonus

    def _calculate_sample_bonus(self, sample_size):
        """
        Small helper: gives a bonus if the sample size is reasonably large.
        sample_size may be a string like "60" or "not reported".
        """
        if not sample_size:
            return 0

        try:
            size = int(str(sample_size).strip())
        except ValueError:
            return 0

        if size >= LARGE_SAMPLE_THRESHOLD:
            return LARGE_SAMPLE_BONUS

        return 0

    def compare_quality_across_studies(self, validated_evidence):
        """
        Step 2: Score every study, and calculate the average quality
        score across all of them.
        """
        self.study_scores = [
            self.evaluate_study_quality(study) for study in validated_evidence
        ]

        if not self.study_scores:
            self.average_score = 0
        else:
            self.average_score = sum(self.study_scores) / len(self.study_scores)

        return self.average_score

    def classify_confidence(self, number_of_studies):
        """
        Step 3: Apply the fixed thresholds to classify overall confidence.
        Also requires a minimum number of studies for "high" confidence,
        even if the average score is high.
        """
        if self.average_score >= CONFIDENCE_THRESHOLDS["high"] and (
            number_of_studies >= MIN_STUDIES_FOR_HIGH_CONFIDENCE
        ):
            self.confidence_level = "high"
        elif self.average_score >= CONFIDENCE_THRESHOLDS["moderate"]:
            self.confidence_level = "moderate"
        elif self.average_score >= CONFIDENCE_THRESHOLDS["low"]:
            self.confidence_level = "low"
        else:
            self.confidence_level = "very low"

        return self.confidence_level

    def build_explanation(self, number_of_studies):
        """
        Step 4: Build a short, human-readable explanation of the rating.
        """
        self.explanation = (
            f"Confidence rated as '{self.confidence_level}' based on "
            f"{number_of_studies} validated stud"
            f"{'y' if number_of_studies == 1 else 'ies'}, "
            f"with an average quality score of {round(self.average_score, 2)}."
        )
        return self.explanation

    def process(self, validated_evidence):
        """
        Convenience method that runs all steps in order.
        Returns a dict with the overall confidence level and explanation.
        """
        number_of_studies = len(validated_evidence)

        self.compare_quality_across_studies(validated_evidence)
        self.classify_confidence(number_of_studies)
        self.build_explanation(number_of_studies)

        return {
            "confidence_level": self.confidence_level,
            "explanation": self.explanation,
            "average_score": self.average_score,
        }



if __name__ == "__main__":
    # Sample validated evidence, built by hand so we know exactly
    # what the correct confidence rating should be.
    sample_validated_evidence = [
        {
            "pmid": "2001",
            "extracted_data": {
                "study_design": "systematic review",
                "sample_size": "120",
            },
        },
        {
            "pmid": "2002",
            "extracted_data": {
                "study_design": "randomized controlled trial",
                "sample_size": "60",
            },
        },
        {
            "pmid": "2003",
            "extracted_data": {
                "study_design": "randomized controlled trial",
                "sample_size": "45",
            },
        },
    ]

    engine = EvidenceConfidenceEngine()
    result = engine.process(sample_validated_evidence)

    print("Component 7 ran successfully!")
    print("Confidence level:", result["confidence_level"])
    print("Average score:", result["average_score"])
    print("Explanation:", result["explanation"])