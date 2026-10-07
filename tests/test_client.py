"""Exercise the GENERATED client against the RUNNING v2 service (real HTTP, no mocks)."""
import socket
import subprocess
import sys
import time

import httpx
import pytest

from client import Client
from client.api.default import create_claim, get_claim, list_claims
from client.models import Claim, ClaimCreate, Status


@pytest.fixture(scope="module")
def client():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "claims_api.v2:app", "--port", str(port), "--log-level", "warning"]
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(50):
            try:
                httpx.get(f"{url}/openapi.json", timeout=0.5)
                break
            except httpx.HTTPError:
                time.sleep(0.1)
        else:
            raise RuntimeError("service did not start")
        yield Client(base_url=url)
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_list_returns_typed_models(client):
    claims = list_claims.sync(client=client)
    assert claims and all(isinstance(c, Claim) for c in claims)
    assert isinstance(claims[0].status, Status)
    assert claims[0].amount_cents == 12550


def test_compatible_additions_visible_in_client(client):
    assert len(list_claims.sync(client=client, limit=2)) == 2  # new optional param
    denied = list_claims.sync(client=client, status=Status.DENIED)
    assert denied[0].denial_code == "CO-50"  # new optional field


def test_get_and_not_found(client):
    assert get_claim.sync(client=client, claim_id="clm_001").provider_name == "Riverside Clinic"
    resp = get_claim.sync_detailed(client=client, claim_id="nope")
    assert resp.status_code == 404


def test_create_roundtrip(client):
    created = create_claim.sync(client=client, body=ClaimCreate(member_id="mem_200", amount_cents=999))
    assert created.status == Status.SUBMITTED and created.amount_cents == 999
    assert get_claim.sync(client=client, claim_id=created.id).member_id == "mem_200"
