# Fixed, rule-based weights used to score each retrieved study.
# Higher score = more relevant/higher quality evidence.

STUDY_TYPE_SCORES = {
    "systematic review": 5,
    "meta-analysis": 5,
    "randomized controlled trial": 4,
    "randomized controlled trial, veterinary": 4,
    "review": 2,
    "case reports": 1,
}
DEFAULT_STUDY_TYPE_SCORE = 1

RECENT_YEARS_THRESHOLD = 5   # published within the last 5 years
RECENT_YEAR_BONUS = 2
OLDER_YEAR_BONUS = 0

TOP_EVIDENCE_LIMIT = 10       # max number of studies to keep after ranking