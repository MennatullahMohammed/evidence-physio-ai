import requests
import xml.etree.ElementTree as ET

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


class PubMedService:
    """
    Handles raw communication with the NCBI PubMed E-utilities API.
    This is the only place in the codebase that talks directly to PubMed.
    """

    def search(self, query, max_results=20):
        """
        Submit a search query to PubMed and return a list of matching PMIDs.
        """
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
        }
        response = requests.get(ESEARCH_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["esearchresult"]["idlist"]

    def fetch_details(self, pmid_list):
        """
        Given a list of PMIDs, fetch their full metadata from PubMed
        and return the parsed XML root element.
        """
        if not pmid_list:
            return None

        params = {
            "db": "pubmed",
            "id": ",".join(pmid_list),
            "retmode": "xml",
        }
        response = requests.get(EFETCH_URL, params=params, timeout=15)
        response.raise_for_status()
        return ET.fromstring(response.content)