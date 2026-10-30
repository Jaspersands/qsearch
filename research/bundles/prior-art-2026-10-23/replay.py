"""Write a reproducible structural audit receipt, not a research candidate."""

import hashlib
import json
from pathlib import Path

from scope_witness import evidence


def main():
    root = Path(__file__).resolve().parent
    record = evidence()
    names = ("scope_witness.py", "test_scope_witness.py", "replay.py", "PRIOR_ART_DECISION.md")
    record["source_sha256"] = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names
    }
    target = root / "scope_receipt.json"
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="ascii")
    print(json.dumps({"receipt": str(target), "status": record["status"],
                      "speedup_admitted": record["speedup_admitted"]}))


if __name__ == "__main__":
    main()
