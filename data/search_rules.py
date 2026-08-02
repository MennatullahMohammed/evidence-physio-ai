# Basic, fixed rules that shape how the search query is built.
# These are simple constants for now — can grow into real logic later.

SEARCH_RULES = {
    "publication_years_limit": 10,   # only include studies from the last 10 years
    "preferred_study_types": [
        "randomized controlled trial",
        "systematic review",
        "meta-analysis",
    ],
}