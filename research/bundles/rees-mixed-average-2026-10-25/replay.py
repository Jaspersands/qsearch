"""Regenerate or check the scoped scientific receipt; no quantum execution."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from mixed_average import adjacent_mixed_control, source_plan

ROOT = Path(__file__).resolve().parent
FILES = ("MIXED_AVERAGE.md", "mixed_average.py", "test_mixed_average.py", "replay.py", "HANDOFF.md")
DEPENDENCIES = (
    "rees-coarse-spectrum-2026-10-24/COARSE_SPECTRUM.md",
    "rees-coarse-spectrum-2026-10-24/coarse_spectrum.py",
    "rees-code-support-2026-10-24/CODE_SUPPORT.md",
    "rees-code-support-2026-10-24/code_support.py",
    "rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md",
    "rees-dilation-average-2026-10-25/dilation_average.py",
)


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def record():
    return {
        "status": "CONDITIONAL_LOCAL_COMPOSITION_NOT_INDEPENDENTLY_REVIEWED",
        "sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES},
        "dependency_sha256": {name: hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest() for name in DEPENDENCIES},
        "control": adjacent_mixed_control(),
        "conditional_resource_plan": source_plan(p=131, nilpotency_class=3, rank_cap=3,
            twirl_gap=F(1, 4), error=F(1, 32), receiver_leaves=8, design_size=24,
            cover_order_bits=32),
        "full_repository_validation": False, "quantum_algorithm_executed": False,
        "native_application_established": False, "novelty_established": False,
        "accepted_speedup_candidate": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.dumps(record(), default=encode, sort_keys=True, indent=2, allow_nan=False)+"\n"
    path = ROOT/"receipt.json"
    if args.write:
        path.write_text(data)
    elif json.loads(path.read_text()) != json.loads(data):
        raise SystemExit("receipt mismatch: source, dependency or scientific output changed")
    print(("WROTE " if args.write else "MATCH ")+str(path))


if __name__ == "__main__":
    main()
