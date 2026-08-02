from data.diagnosis_knowledge_base import DIAGNOSIS_KNOWLEDGE_BASE, DEFAULT_KNOWLEDGE_ENTRY


class MissingClinicalInformationEngine:
    """
    Component 2 — Missing Clinical Information Engine

    Responsibilities:
    1. Load the knowledge base entry that matches the patient's diagnosis
    2. Compare the Patient Profile against that entry's checklist
    3. Detect which required fields are missing/empty
    4. Build the final Patient Context (Complete or Incomplete)
    """

    def load_knowledge_entry(self, working_diagnosis):
        """
        Step 1: Find the knowledge base entry that matches this diagnosis.
        Falls back to DEFAULT_KNOWLEDGE_ENTRY if not found.
        """
        diagnosis_key = working_diagnosis.strip().lower()
        self.knowledge_entry = DIAGNOSIS_KNOWLEDGE_BASE.get(
            diagnosis_key, DEFAULT_KNOWLEDGE_ENTRY
        )
        return self.knowledge_entry

    def compare_with_checklist(self, patient):
        """
        Step 2 + 3: Go through each field in the entry's checklist and
        check whether it's empty on the patient object. Stores the list
        of missing field names on self.missing_fields.
        """
        self.missing_fields = []
        checklist = self.knowledge_entry["checklist"]

        for field_name in checklist:
            value = getattr(patient, field_name, None)

            # A field counts as "missing" if it's None, an empty string,
            # or an empty list.
            if value is None or value == "" or value == []:
                self.missing_fields.append(field_name)

        return self.missing_fields

    def build_patient_context(self, patient):
        """
        Step 4: Build the final output dict.
        If there are missing fields -> "Patient Context (Incomplete)"
        If nothing is missing     -> "Complete Patient Context"
        """
        if self.missing_fields:
            status = "incomplete"
        else:
            status = "complete"

        self.patient_context = {
            "status": status,
            "patient": patient,
            "missing_fields": self.missing_fields,
        }
        return self.patient_context

    def process(self, patient):
        """
        Convenience method that runs all steps in order.
        Returns the final patient_context dict.
        """
        self.load_knowledge_entry(patient.working_diagnosis)
        self.compare_with_checklist(patient)
        return self.build_patient_context(patient)



if __name__ == "__main__":
    from app.models.patient import Patient

    # A sample patient with some fields filled and some left empty,
    # so we can see the engine correctly detect the missing ones.
    sample_patient = Patient(
        working_diagnosis="Rotator Cuff Tendinopathy",
        age=47,
        sex="female",
        occupation="Teacher",
        dominant_side="Right",
        activity_level="Moderate",

        onset="Insidious",
        duration="6 weeks",
        mechanism_of_injury="",       # left empty on purpose
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

        active_rom="",                # left empty on purpose
        passive_rom="",
        strength="",
        special_tests=[],             # left empty on purpose
        neuro_screen="",
        movement_analysis="",

        patient_goals=["Return to swimming"],
        fear_avoidance=False,
        occupational_demands="",      # left empty on purpose
        yellow_flags=[],

        visit_frequency="",
        equipment_access="",
        compliance_history="",
    )

    engine = MissingClinicalInformationEngine()
    patient_context = engine.process(sample_patient)

    print("Component 2 ran successfully!")
    print("Status:", patient_context["status"])
    print("Missing fields:", patient_context["missing_fields"])