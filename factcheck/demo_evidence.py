def analyze_claim(claim: str):

    claim = claim.strip()

    if not claim:
        return {
            "verdict": "Insufficient evidence",
            "confidence": None,
            "evidence": [],
            "limitations": [
                "No claim was provided."
            ]
        }

    return {
        "verdict": "Needs verification",
        "confidence": None,
        "evidence": [],
        "limitations": [
            "Live evidence retrieval is not connected yet.",
            "This is a demonstration response.",
            "No factual conclusion is being made."
        ]
    }