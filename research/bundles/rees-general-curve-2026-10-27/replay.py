"""Replay bounded exact public Jacobian witnesses; no quantum execution."""

import argparse
import json
from fractions import Fraction
from pathlib import Path

from curve_certificate import certificate, source_plan


def payload():
    return {"status": "algebra certificates only; no novelty or speedup certification",
            "certificates": [certificate(c, 101) for c in range(1, 7)],
            "large_prime_certificate": certificate(4, 2**61 - 1),
            "conditional_source_plan": source_plan(4, 15, 2**61 - 1,
                Fraction(1, 3), Fraction(1, 100), 10, 50, 120)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = payload()
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    if args.check and json.loads(path.read_text()) != data:
        raise SystemExit("receipt mismatch")
    print(json.dumps({"status": data["status"], "dimensions": [x["dimension"] for x in data["certificates"]],
                      "determinants": [x["minor_determinant_mod_p"] for x in data["certificates"]],
                      "large_prime_gap_certified": data["large_prime_certificate"]["large_prime_gap_certified"],
                      "conditional_source_plan": data["conditional_source_plan"]}, indent=2))


if __name__ == "__main__":
    main()
