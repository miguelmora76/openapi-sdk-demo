"""Synthetic claims. Invented for this demo; not real payer data."""

CLAIMS = [
    {"id": "clm_001", "member_id": "mem_100", "amount": 125.50, "status": "approved",
     "provider_name": "Riverside Clinic", "denial_code": None},
    {"id": "clm_002", "member_id": "mem_101", "amount": 980.00, "status": "denied",
     "provider_name": "Lakeview Imaging", "denial_code": "CO-50"},
    {"id": "clm_003", "member_id": "mem_100", "amount": 42.00, "status": "submitted",
     "provider_name": "Main St Pharmacy", "denial_code": None},
]
