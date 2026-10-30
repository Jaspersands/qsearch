"""Reproduce bounded exact controls and a clearly labelled analytic bound."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from correlated_source import ReesHeisenberg, acquisition_bound


ROOT = Path(__file__).resolve().parent


def build_receipt():
    rows = []
    for p in (3, 5):
        group = ReesHeisenberg(p)
        checked = 0
        for axis in ("X", "Y"):
            for label in range(p):
                for a in group.elements:
                    if group.conjugacy_kernel(axis, label, a) != group.predicted_kernel(axis, label, a):
                        raise AssertionError((p, axis, label, a))
                    checked += 1
        rows.append({"p": p, "group_order": p**4, "exact_kernel_cases": checked})
    return {
        "status": "scoped_correlated_receiver_shortcut_rejected",
        "quantum_execution": False,
        "novelty_claim": False,
        "controls": rows,
        "analytic_large_prime_bound": acquisition_bound(2**61 - 1, 10**6),
        "dependencies": ["numpy (density tests only)", "sympy primality checking"],
        "source_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("correlated_source.py", "test_correlated_source.py", "replay.py")
        },
    }


def encode(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    receipt = json.loads(json.dumps(build_receipt(), default=encode))
    path = ROOT / "receipt.json"
    if args.write:
        path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    if args.check and json.loads(path.read_text()) != receipt:
        raise SystemExit("receipt mismatch")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
