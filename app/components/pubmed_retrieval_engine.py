from app.services.pubmed_service import PubMedService


class PubMedRetrievalEngine:
    """
    Component 4 — PubMed Retrieval Engine

    Responsibilities:
    1. Submit the optimized query to PubMed
    2. Check how many results came back (zero / too few / enough)
    3. Extract structured metadata for each matching article
    4. Flag to the caller whether search expansion should be offered
       (actual human-in-the-loop confirmation happens outside this
       component, e.g. in the UI layer)
    """

    LOW_RESULTS_THRESHOLD = 3  # fewer than this counts as "too few"

    def __init__(self):
        self.service = PubMedService()

    def submit_query(self, query, max_results=20):
        """
        Step 1: Send the query to PubMed and store the returned PMIDs.
        """
        self.pmid_list = self.service.search(query, max_results=max_results)
        return self.pmid_list

    def check_result_count(self):
        """
        Step 2: Decide whether the result count is acceptable, too low,
        or zero. Stores the decision on self.needs_expansion.
        """
        count = len(self.pmid_list)

        if count == 0:
            self.needs_expansion = True
            self.expansion_reason = "zero_results"
        elif count < self.LOW_RESULTS_THRESHOLD:
            self.needs_expansion = True
            self.expansion_reason = "too_few_results"
        else:
            self.needs_expansion = False
            self.expansion_reason = None

        return self.needs_expansion

    def extract_metadata(self):
        """
        Step 3: Fetch full details for each PMID and pull out the
        fields we care about (PMID, title, authors, journal, year,
        abstract, DOI, publication type).
        """
        self.retrieved_evidence = []

        if not self.pmid_list:
            return self.retrieved_evidence

        xml_root = self.service.fetch_details(self.pmid_list)

        for article in xml_root.findall(".//PubmedArticle"):
            self.retrieved_evidence.append({
                "pmid": self._get_text(article, ".//PMID"),
                "title": self._get_text(article, ".//ArticleTitle"),
                "authors": self._get_authors(article),
                "journal": self._get_text(article, ".//Journal/Title"),
                "publication_year": self._get_text(article, ".//PubDate/Year"),
                "abstract": self._get_text(article, ".//AbstractText"),
                "doi": self._get_doi(article),
                "publication_type": self._get_text(article, ".//PublicationType"),
            })

        return self.retrieved_evidence

    # ----------------------------------------------------------------- #
    # Small private helpers for pulling values out of the XML
    # ----------------------------------------------------------------- #

    def _get_text(self, article, path):
        element = article.find(path)
        return element.text if element is not None else None

    def _get_doi(self, article):
        for id_element in article.findall(".//ArticleId"):
            if id_element.get("IdType") == "doi":
                return id_element.text
        return None

    def _get_authors(self, article):
        authors = []
        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            first_name = author.find("ForeName")
            if last_name is not None and first_name is not None:
                authors.append(f"{first_name.text} {last_name.text}")
        return authors

    def process(self, query, max_results=20):
        """
        Convenience method that runs all steps in order.
        Returns a dict with the retrieved evidence and whether
        search expansion should be offered to the physiotherapist.
        """
        self.submit_query(query, max_results=max_results)
        needs_expansion = self.check_result_count()
        evidence = self.extract_metadata()

        return {
            "retrieved_evidence": evidence,
            "needs_expansion": needs_expansion,
            "expansion_reason": self.expansion_reason,
        }



if __name__ == "__main__":
    from app.models.patient import Patient
    from app.components.missing_clinical_information_engine import MissingClinicalInformationEngine
    from app.components.search_strategy_builder import SearchStrategyBuilder

    # Same sample patient used in earlier components' tests.
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

    # Step through the pipeline: Component 2 -> Component 3 -> Component 4.
    engine = MissingClinicalInformationEngine()
    patient_context = engine.process(sample_patient)

    builder = SearchStrategyBuilder()
    query = builder.process(patient_context)
    print("Query used:", query)

    retrieval_engine = PubMedRetrievalEngine()
    result = retrieval_engine.process(query, max_results=5)

    print("\nComponent 4 ran successfully!")
    print("Needs expansion:", result["needs_expansion"])
    print("Number of articles retrieved:", len(result["retrieved_evidence"]))

    if result["retrieved_evidence"]:
        first_article = result["retrieved_evidence"][0]
        print("\nFirst article:")
        print("  Title:", first_article["title"])
        print("  Journal:", first_article["journal"])
        print("  Year:", first_article["publication_year"])