from models.patient import Patient


class PatientInformationManager:
    """
    Component 1 — Patient Information Manager

    Responsibilities:
    1. Collect patient information (raw data coming in)
    2. Validate patient information (make sure required fields are correct)
    3. Normalize patient information (clean up formatting)
    4. Create a standardized Patient Profile (build the Patient object)
    """

    # These are the fields we absolutely must have to proceed.
    # Everything else is optional for now.
    REQUIRED_FIELDS = [
        "working_diagnosis",
        "age",
        "sex",
        "pain_severity",
    ]

    def collect_patient_information(self, raw_data):
        """
        Step 1: Receive the raw patient data and store it on the object.
        raw_data is expected to be a dict, e.g.:
        {
            "working_diagnosis": "Rotator Cuff Tendinopathy",
            "age": 47,
            "sex": "female",
            "pain_severity": 7,
            ...
        }
        """
        self.raw_data = raw_data
        return self.raw_data

    def validate_patient_information(self):
        """
        Step 2: Check that required fields exist and have reasonable values.
        Stores a list of error messages on self.errors.
        Returns True if no errors, False if there are errors.
        """
        self.errors = []

        # Check required fields are present and not empty
        for field_name in self.REQUIRED_FIELDS:
            value = self.raw_data.get(field_name)
            if value is None or value == "":
                self.errors.append(f"Missing required field: {field_name}")

        # If required fields are missing, no point checking their types yet
        if self.errors:
            return False

        # age must be a whole number between 0 and 120
        age = self.raw_data["age"]
        if not isinstance(age, int):
            self.errors.append("age must be a whole number")
        elif age < 0 or age > 120:
            self.errors.append("age must be between 0 and 120")

        # pain_severity must be a number between 0 and 10 (NRS scale)
        pain = self.raw_data["pain_severity"]
        if not isinstance(pain, int):
            self.errors.append("pain_severity must be a whole number")
        elif pain < 0 or pain > 10:
            self.errors.append("pain_severity must be between 0 and 10")

        # sex must be one of these allowed values
        allowed_sex_values = ["male", "female", "other"]
        sex_value = str(self.raw_data["sex"]).strip().lower()
        if sex_value not in allowed_sex_values:
            self.errors.append("sex must be one of: male, female, other")

        return len(self.errors) == 0

    def normalize_patient_information(self):
        """
        Step 3: Clean up the raw data so it's consistent before we build
        the final Patient object. Stores the result on self.normalized_data.
        """
        self.normalized_data = {}

        # Clean text fields: remove extra spaces at start/end and
        # collapse multiple spaces into one.
        def clean_text(value):
            if value is None:
                return ""
            return " ".join(str(value).split())

        self.normalized_data["working_diagnosis"] = clean_text(
            self.raw_data.get("working_diagnosis")
        )
        self.normalized_data["age"] = self.raw_data.get("age")
        self.normalized_data["sex"] = str(self.raw_data.get("sex")).strip().lower()
        self.normalized_data["occupation"] = clean_text(self.raw_data.get("occupation"))
        self.normalized_data["dominant_side"] = clean_text(self.raw_data.get("dominant_side"))
        self.normalized_data["activity_level"] = clean_text(self.raw_data.get("activity_level"))

        self.normalized_data["onset"] = clean_text(self.raw_data.get("onset"))
        self.normalized_data["duration"] = clean_text(self.raw_data.get("duration"))
        self.normalized_data["mechanism_of_injury"] = clean_text(self.raw_data.get("mechanism_of_injury"))
        self.normalized_data["stage_of_healing"] = clean_text(self.raw_data.get("stage_of_healing"))

        self.normalized_data["pain_severity"] = self.raw_data.get("pain_severity")
        self.normalized_data["pain_irritability"] = clean_text(self.raw_data.get("pain_irritability"))
        self.normalized_data["pain_type"] = clean_text(self.raw_data.get("pain_type"))
        self.normalized_data["pain_location"] = clean_text(self.raw_data.get("pain_location"))
        self.normalized_data["pain_behavior"] = clean_text(self.raw_data.get("pain_behavior"))
        self.normalized_data["symptoms"] = self.raw_data.get("symptoms", [])

        self.normalized_data["past_medical_history"] = self.raw_data.get("past_medical_history", [])
        self.normalized_data["past_surgical_history"] = self.raw_data.get("past_surgical_history", [])
        self.normalized_data["comorbidities"] = self.raw_data.get("comorbidities", [])
        self.normalized_data["medications"] = self.raw_data.get("medications", [])
        self.normalized_data["imaging"] = self.raw_data.get("imaging", [])

        self.normalized_data["baseline_function"] = clean_text(self.raw_data.get("baseline_function"))
        self.normalized_data["functional_limitations"] = self.raw_data.get("functional_limitations", [])
        self.normalized_data["outcome_measures"] = self.raw_data.get("outcome_measures", [])

        self.normalized_data["active_rom"] = clean_text(self.raw_data.get("active_rom"))
        self.normalized_data["passive_rom"] = clean_text(self.raw_data.get("passive_rom"))
        self.normalized_data["strength"] = clean_text(self.raw_data.get("strength"))
        self.normalized_data["special_tests"] = self.raw_data.get("special_tests", [])
        self.normalized_data["neuro_screen"] = clean_text(self.raw_data.get("neuro_screen"))
        self.normalized_data["movement_analysis"] = clean_text(self.raw_data.get("movement_analysis"))

        self.normalized_data["patient_goals"] = self.raw_data.get("patient_goals", [])
        self.normalized_data["fear_avoidance"] = bool(self.raw_data.get("fear_avoidance", False))
        self.normalized_data["occupational_demands"] = clean_text(self.raw_data.get("occupational_demands"))
        self.normalized_data["yellow_flags"] = self.raw_data.get("yellow_flags", [])

        self.normalized_data["visit_frequency"] = clean_text(self.raw_data.get("visit_frequency"))
        self.normalized_data["equipment_access"] = clean_text(self.raw_data.get("equipment_access"))
        self.normalized_data["compliance_history"] = clean_text(self.raw_data.get("compliance_history"))

        return self.normalized_data

    def create_patient_profile(self):
        """
        Step 4: Build and return the final Patient object using the
        normalized data. This is the standardized output of this component.
        """
        patient = Patient(**self.normalized_data)
        return patient

    def process(self, raw_data):
        """
        Convenience method that runs all 4 steps in order.
        Returns the final Patient object, or raises a ValueError
        if validation fails.
        """
        self.collect_patient_information(raw_data)

        is_valid = self.validate_patient_information()
        if not is_valid:
            raise ValueError(f"Validation failed: {self.errors}")

        self.normalize_patient_information()
        return self.create_patient_profile()