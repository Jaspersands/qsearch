"""Print analytic certificates; does not create HSP inputs or run a receiver."""

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from source_tree import profile


def encode(value):
    if isinstance(value, Fraction):
        return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator),
                "approximation": float(value)}
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    payload = {
        "kind": "analytic architecture-bound replay, not quantum experiment",
        "profiles": [profile(c, p, n, n) for c, p, n in
                     [(8, 2**127 - 1, 1000), (16, 2**127 - 1, 1000),
                      (32, 2**521 - 1, 1000),
                      (32, 2**521 - 1, 10**6)]],
        "source_sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                          for name in ("source_tree.py", "test_source_tree.py", "replay.py")},
    }
    encoded = json.dumps(payload, default=encode, indent=2) + "\n"
    receipt = root / "receipt.json"
    if args.write:
        receipt.write_text(encoded, encoding="ascii")
        print(f"Wrote analytic certificate: {receipt}")
    elif args.check:
        if receipt.read_text(encoding="ascii") != encoded:
            raise SystemExit("Analytic certificate is stale or differs")
        print("Analytic certificate matches current source and exact calculations")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
