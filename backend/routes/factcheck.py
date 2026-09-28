from fastapi import APIRouter, HTTPException

from backend.schemas import ClaimRequest
from agents.pipeline import run_fact_check

router = APIRouter()


@router.post("/verify")
def verify_claim(request: ClaimRequest):

    claim = request.claim.strip()

    if not claim:
        raise HTTPException(
            status_code=400,
            detail="Claim cannot be empty"
        )

    result = run_fact_check(claim)

    return {
        "claim": result["claim"],
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "explanation": result["explanation"],
        "evidence": result["evidence"],
        "research": result["research"],
        "claims": result.get("claims", [])
    }