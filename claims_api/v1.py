"""API v1 (frozen baseline). Its spec is committed as specs/v1.json."""
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from claims_api.data import CLAIMS


class Status(str, Enum):
    submitted = "submitted"
    approved = "approved"
    denied = "denied"


class Claim(BaseModel):
    id: str
    member_id: str
    amount: float  # dollars
    status: Status


class ClaimCreate(BaseModel):
    member_id: str
    amount: float


app = FastAPI(title="Claims API", version="1.0.0")
_claims = [{k: c[k] for k in ("id", "member_id", "amount", "status")} for c in CLAIMS]


@app.get("/claims", response_model=list[Claim], operation_id="list_claims")
def list_claims(status: Status | None = None):
    return [c for c in _claims if status is None or c["status"] == status.value]


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
