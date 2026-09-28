import re
from typing import Dict, List


def normalize_text(text: str) -> str:
    """Normalize text for simple keyword comparison."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_keywords(text: str) -> set:
    """Extract useful words from text."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were",
        "to", "of", "in", "on", "for", "and", "or",
        "with", "that", "this", "it", "as", "by", "from",
        "at", "be", "has", "have", "had"
    }

    words = normalize_text(text).split()

    return {
        word
        for word in words
        if len(word) > 2 and word not in stop_words
    }


def fact_check_claim(
    claim: str,
    evidence: List[Dict]
) -> Dict:
    """
    Evidence-based Fact-Checker Agent.

    This version does not use OpenAI or any external LLM API.
    It compares important claim terms with retrieved evidence.
    """

    if not evidence:
        return {
            "verdict": "Insufficient evidence",
            "confidence": None,
            "explanation": "No evidence was retrieved."
        }

    usable_evidence = [
        item for item in evidence
        if item.get("snippet")
    ]

    if not usable_evidence:
        return {
            "verdict": "Insufficient evidence",
            "confidence": None,
            "explanation": "Retrieved sources contain no usable text."
        }

    claim_keywords = get_keywords(claim)

    if not claim_keywords:
        return {
            "verdict": "Insufficient evidence",
            "confidence": 0,
            "explanation": "The claim did not contain enough meaningful text for analysis."
        }

    evidence_scores = []

    for item in usable_evidence:

        snippet = item.get("snippet", "")
        evidence_keywords = get_keywords(snippet)

        common_words = claim_keywords.intersection(
            evidence_keywords
        )

        score = len(common_words) / len(claim_keywords)

        evidence_scores.append({
            "score": score,
            "title": item.get("title", "Unknown source"),
            "url": item.get("url", ""),
            "common_words": common_words
        })

    # Highest evidence similarity
    best_evidence = max(
        evidence_scores,
        key=lambda x: x["score"]
    )

    best_score = best_evidence["score"]

    # Average evidence similarity
    average_score = sum(
        item["score"] for item in evidence_scores
    ) / len(evidence_scores)

    # Convert similarity into confidence
    confidence = round(
        min(best_score * 100, 100),
        2
    )

    # Basic evidence-based decision
    if best_score >= 0.70:
        verdict = "Supported"

        explanation = (
            f"The retrieved evidence strongly overlaps with the "
            f"important terms in the claim. The strongest matching "
            f"source is '{best_evidence['title']}'."
        )

    elif best_score >= 0.40:
        verdict = "Insufficient evidence"

        explanation = (
            f"The retrieved evidence contains some information "
            f"related to the claim, but it does not provide enough "
            f"support to confidently establish the claim. "
            f"The strongest matching source is "
            f"'{best_evidence['title']}'."
        )

    else:
        verdict = "Insufficient evidence"

        explanation = (
            "The retrieved evidence does not contain enough "
            "overlapping information to establish the claim."
        )

    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "evidence_analysis": {
            "best_match_score": round(best_score, 3),
            "average_match_score": round(average_score, 3),
            "sources_analyzed": len(usable_evidence)
        }
    }