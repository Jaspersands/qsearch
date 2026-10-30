"""Reproducible source-algebra controls; no native geometric execution."""

import argparse
import hashlib
import json
from pathlib import Path
from random import Random
import sys

from source_split import ROOT, source_split
from double_level_source import extend_split_to_double
from kernel_output import check_split, mod, odd_maximal_order
from sympy import zeros


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    here = Path(__file__).resolve().parent
    order = odd_maximal_order(11)
    records = []
    for factors in ([(2, 5)], [(3, 4)], [(65537, 2)], [(1000000007, 1)],
                    [(1000000009, 1)], [(2, 3), (3, 2), (5, 2)]):
        modulus = 1
        for p, e in factors:
            modulus *= p**e
        actions, costs = source_split(order, modulus, factors, 11, Random(17))
        doubled = extend_split_to_double(order, actions, modulus)
        check_split(order, doubled, 2*modulus)
        if not all(mod(a-b, modulus) == zeros(2) for a, b in zip(actions, doubled)):
            raise ValueError("double-level coordinates changed")
        records.append({**costs, "actions": [[int(x) for x in a] for a in actions],
                        "verified_double_level": 2*modulus})
    imported = set()
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file:
            path = Path(file).resolve()
            if path.suffix == ".py" and path.is_relative_to(ROOT) and path.parent != here:
                imported.add(path)
    dependencies = {ROOT / name for name in (
        "combined-source-independent-review-2026-10-25/REVIEW.md",
        "suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md",
        "double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md")}
    own = ("source_split.py", "test_source_split.py", "replay_source_split.py", "SOURCE_SPLITTING.md")
    return {"status": "SOURCE_ALGEBRA_SPLITTING_REPAIR",
            "review_finding_addressed": "2: initial abstract splitting at m",
            "review_findings_still_open": ["1: native-input preprocessing", "3: bounded geometric source"],
            "independent_review_of_this_repair": False,
            "native_geometry_executed": False, "quantum_execution": False,
            "native_suborder_only_theorem_established": False, "speedup_established": False,
            "deterministic_seed": 17, "source_characteristic": 11, "controls": records,
            "implementation_sha256": {name: digest(here/name) for name in own},
            "dependency_sha256": {str(path.relative_to(ROOT)): digest(path)
                                  for path in sorted(imported | dependencies)}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evidence()
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(encoded)
    if args.check and path.read_text() != encoded:
        sys.exit("receipt mismatch")
    print(json.dumps({"status": result["status"], "controls": len(result["controls"]),
                      "receipt_sha256": hashlib.sha256(encoded.encode()).hexdigest()}, indent=2))
