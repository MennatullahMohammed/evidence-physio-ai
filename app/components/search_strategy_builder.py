from datetime import datetime

from data.diagnosis_knowledge_base import DIAGNOSIS_KNOWLEDGE_BASE, DEFAULT_KNOWLEDGE_ENTRY
from data.search_rules import SEARCH_RULES


class SearchStrategyBuilder:
    """
    Component 3 — Search Strategy Builder

    Responsibilities:
    1. Load the Diagnosis Knowledge Base entry matching the patient's diagnosis
    2. Build the keyword block (keywords + synonyms + MeSH terms)
    3. Add personalization terms based on patient-specific fields
    4. Combine everything with the search rules into a final query string
    """

    def load_knowledge_entry(self, working_diagnosis):
        """
        Step 1: Find the Diagnosis Knowledge Base entry for this diagnosis.
        Falls back to DEFAULT_KNOWLEDGE_ENTRY if not found.
        """
        diagnosis_key = working_diagnosis.strip().lower()
        self.knowledge_entry = DIAGNOSIS_KNOWLEDGE_BASE.get(
            diagnosis_key, DEFAULT_KNOWLEDGE_ENTRY
        )
        return self.knowledge_entry

    def build_keyword_block(self):
        """
        Step 2: Combine keywords, synonyms, and MeSH terms into one
        list of search terms for this diagnosis.
        """
        self.keyword_block = (
            self.knowledge_entry["keywords"]
            + self.knowledge_entry["synonyms"]
            + self.knowledge_entry["mesh_terms"]
        )
        return self.keyword_block

    def build_personalization_terms(self, patient):
        """
        Step 3: Look at the personalization_fields listed for this
        diagnosis, and pull the matching values from the patient object
        (only if they're filled in).
        """
        self.personalization_terms = []

        for field_name in self.knowledge_entry["personalization_fields"]:
            value = getattr(patient, field_name, None)

            if value is None or value == "" or value == []:
                continue

            # A field can be a single value (str) or a list of values.
            if isinstance(value, list):
                self.personalization_terms.extend(value)
            else:
                self.personalization_terms.append(str(value))

        return self.personalization_terms

    def construct_query(self):
        """
        Step 4: Build the final PubMed query string. The diagnosis terms
        are the only mandatory part of the search. Personalization terms
        are NOT included as a mandatory filter, because generic patient
        attributes (like occupation or activity level) are rarely present
        in a paper's title/abstract, and requiring them as AND conditions
        tends to return zero results. They're kept on self for potential
        future use (e.g. re-ranking results), but don't narrow the search.

        Uses a real PubMed date-range tag (start:end[dp]) rather than a
        plain-English phrase, since PubMed does not parse "last N years"
        as text — it requires actual year boundaries.
        """
        # Diagnosis terms are joined with OR (any of them can match)
        diagnosis_part = " OR ".join(self.keyword_block)
        query = f"({diagnosis_part})"

        # Add a publication year filter using a real date range
        years_limit = SEARCH_RULES["publication_years_limit"]
        current_year = datetime.now().year
        start_year = current_year - years_limit
        query += f" AND ({start_year}:{current_year}[dp])"

        self.query = query
        return self.query

    def process(self, patient_context):
        """
        Convenience method that runs all steps in order.
        patient_context is the dict produced by Component 2
        (Missing Clinical Information Engine).
        Returns the final query string.
        """
        patient = patient_context["patient"]

        self.load_knowledge_entry(patient.working_diagnosis)
        self.build_keyword_block()
        self.build_personalization_terms(patient)
        return self.construct_query()


    
if __name__ == "__main__":
    from app.models.patient import Patient
    from app.components.missing_clinical_information_engine import MissingClinicalInformationEngine

    # Same sample patient used in Component 2's test.
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

    # Step through the pipeline: Component 2 first, then Component 3.
    engine = MissingClinicalInformationEngine()
    patient_context = engine.process(sample_patient)

    builder = SearchStrategyBuilder()
    query = builder.process(patient_context)

    print("Component 3 ran successfully!")
    print("Query:", query)