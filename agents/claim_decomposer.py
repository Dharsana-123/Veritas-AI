import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def decompose_claim(claim: str) -> List[str]:
    """
    Break a complex statement into smaller factual claims.
    """

    claim = claim.strip()

    if not claim:
        return []

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return [claim]

    prompt = f"""
You are the Claim Decomposition Agent for VeritasAI.

Break the following statement into separate factual claims
that can be independently verified.

Statement:
{claim}

Rules:
- Return only the claims.
- Put one claim on each line.
- Do not add numbering.
- Do not add explanations.
- If the statement contains only one factual claim,
  return it unchanged.
"""

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        text = response.output_text.strip()

        claims = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return claims if claims else [claim]

    except Exception:
        # If the LLM is unavailable, continue with the
        # original statement rather than stopping the pipeline.
        return [claim]