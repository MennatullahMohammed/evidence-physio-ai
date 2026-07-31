from dataclasses import dataclass
@dataclass
class patient:
    working_diagnose: str
    age: int
    sex: str
    occupation: str
    dominant_side: str
    activity_level: str

    onset: str
    duration: str
    mechanism_of_injury: str
    stage_of_healing: str

    pain_severity: int
    pain_irritability: str
    pain_type: str
    pain_location: str
    pain_behavior: str
    symptoms: list[str]

    past_medical_history: list[str]
    past_surgical_history: list[str]
    comorbidities: list[str]
    medications: list[str]
    imaging: list[str]

    baseline_function: str
    functional_limitations: list[str]
    outcome_measures: list[str]

    active_rom: str
    passive_rom: str
    strength: str
    special_tests: list[str]
    neuro_screen: str
    movement_analysis: str

    patient_goals: list[str]
    fear_avoidance: bool
    occupational_demands: str
    yellow_flags: list[str]

    visit_frequency: str
    equipment_access: str
    compliance_history: str