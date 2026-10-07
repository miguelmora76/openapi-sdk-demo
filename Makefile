export PYTHONPATH := .

.PHONY: specs client compat test serve
specs:   ## re-export specs/v1.json and specs/v2.json from the code
	uv run python scripts/export_specs.py
client:  ## regenerate the typed client from specs/v2.json
	./scripts/generate_client.sh
compat:  ## fail on unacknowledged breaking changes v1 -> v2
	./scripts/check_compat.sh
test:
	uv run pytest -q
serve:
	uv run uvicorn claims_api.v2:app --reload
