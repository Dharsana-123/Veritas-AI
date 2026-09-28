from typing import Dict


def research_claim(claim: str) -> Dict:
    """
    Researcher Agent

    Breaks the user's input into a research task.
    """

    claim = claim.strip()

    return {
        "claim": claim,
        "research_query": claim,
        "task": "Find reliable evidence that supports or contradicts the claim."
    }