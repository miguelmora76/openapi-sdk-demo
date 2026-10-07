"""Guards on the committed artifacts and the breaking-change gate."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
needs_oasdiff = pytest.mark.skipif(shutil.which("oasdiff") is None, reason="oasdiff not installed")


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def test_committed_specs_match_code():
    r = run("python", "scripts/export_specs.py", "--check")
    assert r.returncode == 0, r.stderr


@needs_oasdiff
def test_gate_passes_with_acknowledged_break():
    assert run("scripts/check_compat.sh").returncode == 0


@needs_oasdiff
def test_gate_fails_on_unacknowledged_break():
    r = run("oasdiff", "breaking", "specs/v1.json", "specs/v2.json", "--fail-on", "ERR")
    assert r.returncode == 1 and "response-required-property-removed" in r.stdout


@needs_oasdiff
def test_compatible_changes_are_not_flagged():
    out = run("oasdiff", "breaking", "specs/v1.json", "specs/v2.json").stdout
    assert "limit" not in out and "provider_name" not in out
