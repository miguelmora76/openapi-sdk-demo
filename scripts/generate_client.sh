#!/usr/bin/env bash
# Regenerate the typed Python client from the v2 spec.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf client
uv run openapi-python-client generate --path specs/v2.json --output-path client \
  --meta none --overwrite
