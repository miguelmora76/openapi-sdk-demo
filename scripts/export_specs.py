"""Write each API version's OpenAPI spec to specs/. `--check` fails if committed specs are stale."""
import json
import sys
from pathlib import Path

from claims_api import v1, v2

ROOT = Path(__file__).resolve().parent.parent / "specs"
check = "--check" in sys.argv
stale = []
for name, app in (("v1", v1.app), ("v2", v2.app)):
    text = json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n"
    path = ROOT / f"{name}.json"
    if check:
        if not path.exists() or path.read_text() != text:
            stale.append(path.name)
    else:
        path.write_text(text)
if stale:
    sys.exit(f"stale specs (run `make specs`): {', '.join(stale)}")
