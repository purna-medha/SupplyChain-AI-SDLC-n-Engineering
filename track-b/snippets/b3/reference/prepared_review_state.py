"""A review decision changes draft state; saving and reloading preserves it.

Try: change approved to rejected and inspect the visible notes.
The decision below is supplied classroom input, not production authentication.
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

note = {"id": "D1", "text": "C1 is delayed.", "status": "pending"}
decision = "approved"
print("Before review:", note)

if note["status"] != "pending" or decision not in {"approved", "rejected"}:
    raise ValueError("Expected a pending note and a valid human decision")
note["status"] = decision

with TemporaryDirectory() as directory:
    path = Path(directory) / "review.json"
    path.write_text(json.dumps(note), encoding="utf-8")
    restored = json.loads(path.read_text(encoding="utf-8"))
    visible = [restored] if restored["status"] == "approved" else []
    print("Restored:", restored)
    print("Visible:", visible)
