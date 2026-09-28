from typing import List, Dict


def retrieve_evidence(claim: str) -> List[Dict]:
    """
    Temporary evidence retrieval layer.

    Live web search will be connected in the next step.
    """

    claim = claim.strip()

    if not claim:
        return []

    return [
        {
            "title": "Evidence retrieval placeholder",
            "source": "Not connected yet",
            "url": None,
            "snippet": (
                "Live web evidence retrieval will be connected "
                "in the next development step."
            )
        }
    ]