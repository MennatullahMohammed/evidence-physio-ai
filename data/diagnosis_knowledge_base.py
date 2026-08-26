# Unified Diagnosis Knowledge Base
# Single source of truth for everything related to a diagnosis:
# - checklist          -> used by Component 2 (Missing Clinical Information Engine)
# - keywords/synonyms/mesh_terms/personalization_fields -> used by Component 3 (Search Strategy Builder)

DIAGNOSIS_KNOWLEDGE_BASE = {
    "rotator cuff tendinopathy": {
    "checklist": [
        "onset",
        "mechanism_of_injury",
        "pain_irritability",
        "active_rom",
        "special_tests",
        "occupational_demands",
    ],
    "keywords": [
        "rotator cuff tendinopathy",
        "shoulder impingement",
        "subacromial impingement",
    ],
    "synonyms": [
        "supraspinatus tendinopathy",
        "rotator cuff tendinitis",
        "shoulder tendinopathy",
    ],
    "mesh_terms": [
        "Rotator Cuff Injuries",
        "Shoulder Impingement Syndrome",
    ],
    "personalization_fields": ["occupation", "activity_level", "dominant_side"],
    },
    "low back pain": {
        "checklist": [
            "onset",
            "mechanism_of_injury",
            "pain_behavior",
            "yellow_flags",
            "neuro_screen",
            "functional_limitations",
        ],
        "keywords": ["low back pain", "lumbar pain"],
        "synonyms": ["non-specific low back pain"],
        "mesh_terms": ["Lumbosacral Region"],
        "personalization_fields": ["occupational_demands", "yellow_flags", "activity_level"],
    },
    # Add more diagnoses here as needed.
}

# Used when a diagnosis is not found in DIAGNOSIS_KNOWLEDGE_BASE above.
DEFAULT_KNOWLEDGE_ENTRY = {
    "checklist": [
        "onset",
        "mechanism_of_injury",
        "pain_irritability",
        "functional_limitations",
    ],
    "keywords": [],
    "synonyms": [],
    "mesh_terms": [],
    "personalization_fields": [],
}