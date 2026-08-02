from app.services.claude_synthesis_service import ClaudeSynthesisService


class EvidenceSynthesisEngine:
    """
    Component 8 — Evidence Synthesis Engine

    Responsibilities:
    1. Format the validated evidence into a plain-text summary block
    2. Analyze the evidence against the patient's context (via Claude)
    3. Generate a patient-specific evidence summary
    """

    def __init__(self):
        self.service = ClaudeSynthesisService()

    def format_evidence_summaries(self, validated_evidence):
        """
        Step 1: Turn the list of validated evidence into a simple
        numbered text block Claude can read easily.
        """
        lines = []
        for index, study in enumerate(validated_evidence, start=1):
            extracted = study.get("extracted_data", {})
            lines.append(
                f"{index}. Population: {extracted.get('population', 'N/A')} | "
                f"Intervention: {extracted.get('intervention', 'N/A')} | "
                f"Outcome: {extracted.get('outcome', 'N/A')} | "
                f"Key findings: {extracted.get('key_findings', 'N/A')}"
            )

        self.evidence_summaries = "\n".join(lines)
        return self.evidence_summaries

    def generate_summary(self, patient, confidence_level):
        """
        Step 2 + 3: Send the formatted evidence and patient context
        to Claude, and store the resulting patient-specific summary.
        """
        self.patient_specific_summary = self.service.synthesize(
            patient=patient,
            confidence_level=confidence_level,
            evidence_summaries=self.evidence_summaries,
        )
        return self.patient_specific_summary

    def process(self, validated_evidence, patient, confidence_level):
        """
        Convenience method that runs all steps in order.
        Returns the patient-specific evidence summary text.
        """
        self.format_evidence_summaries(validated_evidence)
        return self.generate_summary(patient, confidence_level)



if __name__ == "__main__":
    from app.models.patient import Patient

    sample_patient = Patient(
        working_diagnosis="Rotator Cuff Tendinopathy",
        age=47,
        sex="female",
        occupation="Teacher",
        dominant_side="Right",
        activity_level="Moderate",
        onset="Insidious",
        duration="6 weeks",
        mechanism_of_injury="",
        stage_of_healing="",
        pain_severity=7,
        pain_irritability="High",
        pain_type="",
        pain_location="Lateral shoulder",
        pain_behavior="",
        symptoms=["Night pain"],
        past_medical_history=[],
        past_surgical_history=[],
        comorbidities=[],
        medications=["NSAIDs"],
        imaging=[],
        baseline_function="",
        functional_limitations=["Cannot lift arm above shoulder"],
        outcome_measures=[],
        active_rom="",
        passive_rom="",
        strength="",
        special_tests=[],
        neuro_screen="",
        movement_analysis="",
        patient_goals=["Return to swimming"],
        fear_avoidance=False,
        occupational_demands="",
        yellow_flags=[],
        visit_frequency="",
        equipment_access="",
        compliance_history="",
    )

    sample_validated_evidence = [
        {
            "pmid": "9999999",
            "extracted_data": {
                "population": "Adults with chronic rotator cuff tendinopathy",
                "intervention": "12-week eccentric exercise program",
                "comparison": "standard physiotherapy care",
                "outcome": "shoulder pain and function scores",
                "sample_size": "60",
                "study_design": "randomized controlled trial",
                "key_findings": "Eccentric exercise showed significantly greater improvement than standard care.",
            },
        },
    ]

    engine = EvidenceSynthesisEngine()

    try:
        summary = engine.process(
            validated_evidence=sample_validated_evidence,
            patient=sample_patient,
            confidence_level="moderate",
        )
        print("Component 8 ran successfully!")
        print("Summary:", summary)
    except Exception as e:
        print("Component 8 raised an error (expected if API credit is low):")
        print(e)    