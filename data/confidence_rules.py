# Fixed, rule-based criteria for classifying overall evidence confidence.
# No AI model is involved — this is deterministic and explainable by design.

# Points awarded per study, based on its study design quality.
STUDY_QUALITY_POINTS = {
    "systematic review": 4,
    "meta-analysis": 4,
    "randomized controlled trial": 3,
    "review": 2,
    "case reports": 1,
}
DEFAULT_QUALITY_POINTS = 1

# Bonus points if a study reports a reasonably large sample size.
LARGE_SAMPLE_THRESHOLD = 50
LARGE_SAMPLE_BONUS = 1

# Thresholds for the overall confidence rating, based on the
# average quality score across all validated studies.
CONFIDENCE_THRESHOLDS = {
    "high": 4.0,       # average score >= 4.0
    "moderate": 2.5,    # average score >= 2.5
    "low": 1.0,        # average score >= 1.0
    # anything below "low" threshold -> "very low"
}

MIN_STUDIES_FOR_HIGH_CONFIDENCE = 3