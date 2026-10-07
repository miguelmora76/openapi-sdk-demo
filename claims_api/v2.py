"""API v2 (current). Spec is committed as specs/v2.json and the client is generated from it.

Changes vs v1:
  * BACKWARD-COMPATIBLE: new optional `limit` query param on GET /claims, and new
    optional response field `provider_name` (plus `denial_code`) on Claim.
  * BREAKING (deliberate): Claim.`amount` (float dollars) is replaced by
    Claim.`amount_cents` (int). Existing clients reading `amount` would break.
"""
from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from claims_api.data import CLAIMS


class Status(str, Enum):
    submitted = "submitted"
    approved = "approved"
    denied = "denied"


class Claim(BaseModel):
    id: str
    member_id: str
    amount_cents: int  # BREAKING: was `amount: float` in v1
    status: Status
    provider_name: str | None = None  # compatible: new optional field
    denial_code: str | None = None  # compatible: new optional field


class ClaimCreate(BaseModel):
    member_id: str
    amount_cents: int  # BREAKING (request side): was `amount: float`


app = FastAPI(title="Claims API", version="2.0.0")
_claims = [
    {**c, "amount_cents": round(c["amount"] * 100)} for c in CLAIMS
]


@app.get("/claims", response_model=list[Claim], operation_id="list_claims")
def list_claims(
    status: Status | None = None,
    limit: int | None = Query(None, ge=1, le=100),  # compatible: new optional param
):
    out = [c for c in _claims if status is None or c["status"] == status.value]
    return out[:limit] if limit else out


@app.get("/claims/{claim_id}", response_model=Claim, operation_id="get_claim")
def get_claim(claim_id: str):
    for c in _claims:
        if c["id"] == claim_id:
            return c
    raise HTTPException(404, "claim not found")


@app.post("/claims", response_model=Claim, status_code=201, operation_id="create_claim")
def create_claim(body: ClaimCreate):
    claim = {"id": f"clm_{len(_claims) + 1:03d}", "status": "submitted", **body.model_dump()}
    _claims.append(claim)
    return claim
