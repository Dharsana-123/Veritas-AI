from pydantic import BaseModel


class ClaimRequest(BaseModel):
    claim: str