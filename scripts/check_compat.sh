#!/usr/bin/env bash
# Fail on any breaking change between v1 and v2 that is not listed in specs/breaking-ack.txt.
set -euo pipefail
cd "$(dirname "$0")/.."
oasdiff breaking specs/v1.json specs/v2.json --fail-on ERR --err-ignore specs/breaking-ack.txt
