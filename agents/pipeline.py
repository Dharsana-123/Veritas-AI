from agents.claim_decomposer import decompose_claim
from agents.researcher import research_claim
from agents.retriever import retrieve_sources
from agents.fact_checker import fact_check_claim


def run_fact_check(claim: str):
    """
    Run the complete VeritasAI fact-checking workflow.
    """

    # Step 1: Decompose the input
    claims = decompose_claim(claim)

    results = []

    # Step 2: Fact-check each individual claim
    for individual_claim in claims:

        research_task = research_claim(
            individual_claim
        )

        evidence = retrieve_sources(
            research_task
        )

        assessment = fact_check_claim(
            individual_claim,
            evidence
        )

        results.append(
            {
                "claim": individual_claim,
                "research": research_task,
                "evidence": evidence,
                "assessment": assessment
            }
        )

    # Preserve the old response structure
    # for compatibility with the current frontend.
    if len(results) == 1:

        result = results[0]

        return {
            "claim": claim,
            "verdict": result["assessment"]["verdict"],
            "confidence": result["assessment"]["confidence"],
            "explanation": result["assessment"]["explanation"],
            "evidence": result["evidence"],
            "research": result["research"],
            "claims": results
        }

    return {
        "claim": claim,
        "verdict": "Multiple claims assessed",
        "confidence": None,
        "explanation": (
            f"VeritasAI identified {len(results)} "
            "individual claims for assessment."
        ),
        "evidence": [
            evidence_item
            for result in results
            for evidence_item in result["evidence"]
        ],
        "research": {
            "claim_count": len(results)
        },
        "claims": results
    }