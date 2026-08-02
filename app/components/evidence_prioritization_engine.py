from datetime import datetime

from data.scoring_rules import (
    STUDY_TYPE_SCORES,
    DEFAULT_STUDY_TYPE_SCORE,
    RECENT_YEARS_THRESHOLD,
    RECENT_YEAR_BONUS,
    OLDER_YEAR_BONUS,
    TOP_EVIDENCE_LIMIT,
)


class EvidencePrioritizationEngine:
    """
    Component 5 — Evidence Prioritization Engine

    Responsibilities:
    1. Remove duplicate studies (same PMID)
    2. Calculate a rule-based relevance score for each study
    3. Rank studies by that score
    4. Select the top evidence (and flag if evidence is limited)
    """

    LOW_EVIDENCE_THRESHOLD = 3  # fewer than this counts as "limited evidence"

    def remove_duplicates(self, retrieved_evidence):
        """
        Step 1: Keep only one entry per PMID.
        """
        seen_pmids = set()
        self.deduplicated_evidence = []

        for study in retrieved_evidence:
            pmid = study.get("pmid")
            if pmid not in seen_pmids:
                seen_pmids.add(pmid)
                self.deduplicated_evidence.append(study)

        return self.deduplicated_evidence

    def calculate_relevance_score(self, study):
        """
        Step 2 (per study): Combine a study-type score and a
        recency score into one total relevance score.
        """
        study_type = (study.get("publication_type") or "").strip().lower()
        type_score = STUDY_TYPE_SCORES.get(study_type, DEFAULT_STUDY_TYPE_SCORE)

        year_score = self._calculate_year_score(study.get("publication_year"))

        return type_score + year_score

    def _calculate_year_score(self, publication_year):
        """
        Small helper: gives a bonus if the study was published recently.
        """
        if not publication_year:
            return OLDER_YEAR_BONUS

        try:
            year = int(publication_year)
        except ValueError:
            return OLDER_YEAR_BONUS

        current_year = datetime.now().year
        if (current_year - year) <= RECENT_YEARS_THRESHOLD:
            return RECENT_YEAR_BONUS

        return OLDER_YEAR_BONUS

    def rank_studies(self):
        """
        Step 3: Score every study in self.deduplicated_evidence, attach
        the score to each one, and sort them from highest to lowest.
        """
        scored_evidence = []

        for study in self.deduplicated_evidence:
            score = self.calculate_relevance_score(study)
            study_with_score = dict(study)  # copy, don't mutate the original
            study_with_score["relevance_score"] = score
            scored_evidence.append(study_with_score)

        self.ranked_evidence = sorted(
            scored_evidence, key=lambda s: s["relevance_score"], reverse=True
        )
        return self.ranked_evidence

    def select_top_evidence(self):
        """
        Step 4: Keep only the top N studies (TOP_EVIDENCE_LIMIT), and
        flag whether the total evidence available is limited.
        """
        self.prioritized_evidence = self.ranked_evidence[:TOP_EVIDENCE_LIMIT]
        self.limited_evidence = len(self.ranked_evidence) < self.LOW_EVIDENCE_THRESHOLD

        return self.prioritized_evidence

    def process(self, retrieved_evidence):
        """
        Convenience method that runs all steps in order.
        Returns a dict with the prioritized evidence and whether
        the available evidence is limited.
        """
        self.remove_duplicates(retrieved_evidence)
        self.rank_studies()
        self.select_top_evidence()

        return {
            "prioritized_evidence": self.prioritized_evidence,
            "limited_evidence": self.limited_evidence,
        }



if __name__ == "__main__":
    from datetime import datetime

    current_year = datetime.now().year
    recent_year = str(current_year - 1)   # 1 year ago -> recent
    old_year = str(current_year - 15)      # 15 years ago -> not recent

    # Sample evidence, built by hand so we know exactly what the
    # correct ranking should look like.
    sample_evidence = [
        {
            "pmid": "1001",
            "title": "Old case report on shoulder pain",
            "publication_type": "case reports",
            "publication_year": old_year,
        },
        {
            "pmid": "1002",
            "title": "Recent systematic review on rotator cuff treatment",
            "publication_type": "systematic review",
            "publication_year": recent_year,
        },
        {
            "pmid": "1002",  # duplicate PMID on purpose
            "title": "Recent systematic review on rotator cuff treatment",
            "publication_type": "systematic review",
            "publication_year": recent_year,
        },
        {
            "pmid": "1003",
            "title": "Study with unknown publication type",
            "publication_type": "",
            "publication_year": recent_year,
        },
        {
            "pmid": "1004",
            "title": "Recent randomized controlled trial",
            "publication_type": "randomized controlled trial",
            "publication_year": recent_year,
        },
    ]

    engine = EvidencePrioritizationEngine()
    result = engine.process(sample_evidence)

    print("Component 5 ran successfully!")
    print("Limited evidence:", result["limited_evidence"])
    print("Number of prioritized studies:", len(result["prioritized_evidence"]))
    print("\nRanking (highest to lowest score):")
    for study in result["prioritized_evidence"]:
        print(f"  Score {study['relevance_score']} — {study['title']}")