"""Replay the matrix-only lift on a frozen native matrix artifact."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from point_lift import lift_point


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "ag-divisor-class-control-2026-10-26/receipt.json"
SOURCE_HASH = "a0b6db4bc55c6097da5b65db49b654088c0a4d20747d3e50ee1d822386c2bc63"


def report():
    if sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_HASH:
        raise ValueError("frozen native matrix artifact changed")
    native = json.loads(SOURCE.read_text())["control"]
    result = lift_point(native["original_parity"], native["prime"])
    sources = [ROOT / name for name in ("point_lift.py", "test_point_lift.py", "verify_lift.py", "LIFT.md")]
    sources.append(SOURCE)
    return {"status": "MATRIX_ONLY_GEOMETRIC_LIFT_UNDER_COMPLETE_AG_PROMISE",
            "result": result,
            "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                       for path in sources}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    destination = ROOT / "receipt.json"
    if args.write:
        destination.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        if json.loads(destination.read_text()) != result:
            raise SystemExit("FAIL: matrix-only point-lift replay differs")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: {len(result['sha256'])} hashes; SHA256 {sha256(destination.read_bytes()).hexdigest()}")
