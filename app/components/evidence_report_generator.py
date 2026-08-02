import json
from datetime import datetime, timezone

from app.models.patient import Patient


class EvidenceReportGenerator:
    """
    Component 10 — Evidence Report Generator

    Responsibilities:
    1. Collect the outputs of all previous components
    2. Assemble them into a structured report with these sections:
       patient summary, search strategy, selected studies,
       evidence confidence, patient-specific evidence summary,
       natural language explanation, references
    3. Produce a machine-readable JSON version
    4. Produce a human-readable text version
    """

    def build_patient_summary_section(self, patient: Patient):
        """
        Step: Build a short patient summary section from the Patient object.
        """
        self.patient_summary = {
            "working_diagnosis": patient.working_diagnosis,
            "age": patient.age,
            "sex": patient.sex,
            "pain_severity": patient.pain_severity,
            "functional_limitations": patient.functional_limitations,
            "patient_goals": patient.patient_goals,
        }
        return self.patient_summary

    def build_search_strategy_section(self, query):
        """
        Step: Store the PubMed query used for this report.
        """
        self.search_strategy = {"query": query}
        return self.search_strategy

    def build_selected_studies_section(self, prioritized_evidence):
        """
        Step: Build a simplified list of the studies that were selected,
        for quick reference in the report.
        """
        self.selected_studies = [
            {
                "pmid": study.get("pmid"),
                "title": study.get("title"),
                "journal": study.get("journal"),
                "publication_year": study.get("publication_year"),
                "relevance_score": study.get("relevance_score"),
            }
            for study in prioritized_evidence
        ]
        return self.selected_studies

    def build_references_section(self, prioritized_evidence):
        """
        Step: Build a simple reference list (title, authors, journal, year, doi).
        """
        self.references = [
            {
                "pmid": study.get("pmid"),
                "title": study.get("title"),
                "authors": study.get("authors"),
                "journal": study.get("journal"),
                "publication_year": study.get("publication_year"),
                "doi": study.get("doi"),
            }
            for study in prioritized_evidence
        ]
        return self.references

    def assemble_report(
        self,
        patient,
        query,
        prioritized_evidence,
        validated_evidence,
        confidence_result,
        patient_specific_summary,
        natural_language_explanation,
    ):
        """
        Combines all sections into one structured report dict.
        """
        self.build_patient_summary_section(patient)
        self.build_search_strategy_section(query)
        self.build_selected_studies_section(prioritized_evidence)
        self.build_references_section(prioritized_evidence)

        self.report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "patient_summary": self.patient_summary,
            "search_strategy": self.search_strategy,
            "selected_studies": self.selected_studies,
            "evidence_confidence": confidence_result,
            "patient_specific_evidence_summary": patient_specific_summary,
            "natural_language_explanation": natural_language_explanation,
            "references": self.references,
            # Kept for completeness, even though it's not shown in the
            # human-readable version (too detailed for a quick read).
            "validated_evidence": validated_evidence,
        }
        return self.report

    def to_json(self):
        """
        Produces the machine-readable JSON version of the report.
        """
        return json.dumps(self.report, indent=2)

    def to_human_readable_text(self):
        """
        Produces the human-readable text version of the report.
        """
        p = self.report["patient_summary"]
        lines = []

        lines.append("=" * 60)
        lines.append("EVIDENCEPHYSIO AI — CLINICAL EVIDENCE REPORT")
        lines.append("=" * 60)

        lines.append("\n--- PATIENT SUMMARY ---")
        lines.append(f"Working diagnosis: {p['working_diagnosis']}")
        lines.append(f"Age: {p['age']} | Sex: {p['sex']}")
        lines.append(f"Pain severity (NRS): {p['pain_severity']}/10")
        lines.append(f"Functional limitations: {', '.join(p['functional_limitations']) or 'None reported'}")
        lines.append(f"Patient goals: {', '.join(p['patient_goals']) or 'None reported'}")

        lines.append("\n--- SEARCH STRATEGY ---")
        lines.append(self.report["search_strategy"]["query"])

        lines.append("\n--- SELECTED STUDIES ---")
        for study in self.report["selected_studies"]:
            lines.append(
                f"  - [{study['pmid']}] {study['title']} "
                f"({study['journal']}, {study['publication_year']}) "
                f"— score: {study['relevance_score']}"
            )
        if not self.report["selected_studies"]:
            lines.append("  No studies were selected.")

        lines.append("\n--- EVIDENCE CONFIDENCE ---")
        confidence = self.report["evidence_confidence"]
        lines.append(f"Level: {confidence.get('confidence_level')}")
        lines.append(f"Explanation: {confidence.get('explanation')}")

        lines.append("\n--- PATIENT-SPECIFIC EVIDENCE SUMMARY ---")
        lines.append(self.report["patient_specific_evidence_summary"] or "Not available.")

        lines.append("\n--- NATURAL LANGUAGE EXPLANATION ---")
        lines.append(self.report["natural_language_explanation"] or "Not available.")

        lines.append("\n--- REFERENCES ---")
        for ref in self.report["references"]:
            lines.append(f"  - {ref['title']} ({ref['journal']}, {ref['publication_year']}) DOI: {ref['doi']}")
        if not self.report["references"]:
            lines.append("  No references available.")

        return "\n".join(lines)

    def process(
        self,
        patient,
        query,
        prioritized_evidence,
        validated_evidence,
        confidence_result,
        patient_specific_summary,
        natural_language_explanation,
    ):
        """
        Convenience method that runs all steps in order.
        Returns a dict with both the JSON and human-readable versions.
        """
        self.assemble_report(
            patient=patient,
            query=query,
            prioritized_evidence=prioritized_evidence,
            validated_evidence=validated_evidence,
            confidence_result=confidence_result,
            patient_specific_summary=patient_specific_summary,
            natural_language_explanation=natural_language_explanation,
        )

        return {
            "json_report": self.to_json(),
            "human_readable_report": self.to_human_readable_text(),
        }



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

    sample_query = "(rotator cuff tendinopathy OR shoulder impingement) AND (last 10 years[dp])"

    sample_prioritized_evidence = [
        {
            "pmid": "9999999",
            "title": "Effectiveness of eccentric exercise for rotator cuff tendinopathy",
            "authors": ["Jane Smith", "John Doe"],
            "journal": "Journal of Physiotherapy",
            "publication_year": "2022",
            "doi": "10.1000/example.doi",
            "relevance_score": 7,
        },
    ]

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

    sample_confidence_result = {
        "confidence_level": "moderate",
        "explanation": "Confidence rated as 'moderate' based on 1 validated study, with an average quality score of 4.0.",
        "average_score": 4.0,
    }

    sample_patient_specific_summary = (
        "For this 47-year-old patient with rotator cuff tendinopathy, "
        "evidence suggests eccentric exercise may improve pain and function "
        "more than standard care alone."
    )

    sample_natural_language_explanation = (
        "The evidence found is moderately reliable, coming from a single "
        "randomized controlled trial. While promising, more studies would "
        "strengthen confidence in this recommendation."
    )

    generator = EvidenceReportGenerator()
    result = generator.process(
        patient=sample_patient,
        query=sample_query,
        prioritized_evidence=sample_prioritized_evidence,
        validated_evidence=sample_validated_evidence,
        confidence_result=sample_confidence_result,
        patient_specific_summary=sample_patient_specific_summary,
        natural_language_explanation=sample_natural_language_explanation,
    )

    print("Component 10 ran successfully!\n")
    print(result["human_readable_report"])