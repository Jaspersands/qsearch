"""Replay forced-symmetry controls without claiming geometric execution."""

import argparse
import hashlib
import json
from pathlib import Path

from inherited_symmetries import control

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def receipt():
    paths = [HERE / name for name in (
        "INHERITED_SYMMETRIES.md", "inherited_symmetries.py",
        "test_inherited_symmetries.py", "replay_symmetries.py",
    )]
    paths += [ROOT / name for name in (
        "interpolation-leakage-2026-10-26/interpolation_closure.py",
        "interpolation-leakage-2026-10-26/receipt.json",
        "ppav-source-2026-10-23/2026-1142.pdf",
    )]
    return {
        "schema": "partial-quotient-inherited-symmetries-v1",
        "status": "structural negative control, not a failed native attack",
        "controls": [control(q, (1, 2, 1, 1), divisor)
                     for q, divisor in ((3, 2), (5, 4), (17, 6), (17, 24))],
        "all_native_geometry_unexecuted": True,
        "independent_review": False,
        "native_classical_hardness_or_quantum_advantage": False,
        "hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in paths},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    if args.check and json.loads(path.read_text()) != result:
        raise SystemExit("receipt mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
