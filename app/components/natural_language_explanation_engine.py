from app.services.claude_explanation_service import ClaudeExplanationService


class NaturalLanguageExplanationEngine:
    """
    Component 9 — Natural Language Explanation Engine

    Responsibilities:
    1. Take the patient-specific evidence summary and confidence rating
    2. Translate them into a clear, natural-language explanation
       for the physiotherapist (via Claude)
    3. Ensure limitations and uncertainties are highlighted in
       clinician-friendly language
    """

    def __init__(self):
        self.service = ClaudeExplanationService()

    def generate_explanation(self, patient_specific_summary, confidence_level, confidence_explanation):
        """
        Steps 1-3: Send the summary and confidence info to Claude,
        and store the resulting natural-language explanation.
        """
        self.natural_language_explanation = self.service.explain(
            patient_specific_summary=patient_specific_summary,
            confidence_level=confidence_level,
            confidence_explanation=confidence_explanation,
        )
        return self.natural_language_explanation

    def process(self, patient_specific_summary, confidence_level, confidence_explanation):
        """
        Convenience method that runs the explanation generation step.
        Returns the natural-language explanation text.
        """
        return self.generate_explanation(
            patient_specific_summary=patient_specific_summary,
            confidence_level=confidence_level,
            confidence_explanation=confidence_explanation,
        )



if __name__ == "__main__":
    sample_summary = (
        "For this 47-year-old patient with rotator cuff tendinopathy, "
        "evidence from a randomized controlled trial suggests that a "
        "12-week eccentric exercise program leads to significantly "
        "greater improvement in shoulder pain and function compared "
        "to standard physiotherapy care."
    )

    engine = NaturalLanguageExplanationEngine()

    try:
        explanation = engine.process(
            patient_specific_summary=sample_summary,
            confidence_level="moderate",
            confidence_explanation=(
                "Confidence rated as 'moderate' based on 3 validated "
                "studies, with an average quality score of 4.0."
            ),
        )
        print("Component 9 ran successfully!")
        print("Explanation:", explanation)
    except Exception as e:
        print("Component 9 raised an error (expected if API credit is low):")
        print(e)