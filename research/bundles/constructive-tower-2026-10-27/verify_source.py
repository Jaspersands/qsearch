"""Bound and seed replay only: no function-field generation is implemented."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from source_controls import prime_class_bound, seed_kernel

ROOT = Path(__file__).resolve().parent


def jsonable(value):
    if isinstance(value, Fraction):
        return {"numerator_hex": hex(value.numerator),
                "denominator_hex": hex(value.denominator)}
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def report():
    sources = [ROOT/name for name in ("SOURCE.md", "PRIME_CLASS.md", "ARITHMETIC.md",
                                    "REVIEW_RESOLUTION.md", "source_controls.py",
                                    "test_source_controls.py", "verify_source.py")]
    sources += [ROOT.parent/"generic-divisor-class-2026-10-26/class_bound.py",
                ROOT.parent/"prime-ag-tower-source-2026-10-26/tower_seed.py"]
    return jsonable({
        "status": "SOURCE_REDUCTION_CONTROLS_NOT_IMPLEMENTED_GENERATOR",
        "prime_class_certificates": [prime_class_bound(e) for e in (8, 16, 32, 64)],
        "actual_seed_kummer_kernel": seed_kernel(),
        "native_higher_level_constructed": False,
        "quantum_advantage_established": False,
        "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                   for path in sources},
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    path = ROOT/"receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        if json.loads(path.read_text()) != result:
            raise SystemExit("FAIL: source controls differ")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: {len(result['sha256'])} hashes; SHA256 {sha256(path.read_bytes()).hexdigest()}")
