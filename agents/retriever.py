from typing import Dict, List

from factcheck.evidence import retrieve_evidence


def retrieve_sources(research_task: Dict) -> List[Dict]:
    """
    Retriever Agent

    Uses the evidence retrieval layer to collect sources.
    """

    query = research_task["research_query"]

    evidence = retrieve_evidence(query)

    return evidence