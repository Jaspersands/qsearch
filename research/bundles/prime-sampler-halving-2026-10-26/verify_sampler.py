"""Replay the weaker sampling contract, retaining exact-order access debt."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from sampler_contract import prime_sampling_certificate, relation_batch_bound


ROOT = Path(__file__).resolve().parent


def encode(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)


def report():
    degrees = [prime_sampling_certificate(g) for g in (1, 6, 41, 81, 161, 321, 641, 10**4, 10**8, 10**16)]
    batches = [relation_batch_bound(t) for t in range(101)]
    assert all(row["exact_sufficiency_ratio"] >= 1 and row["fits_recovered_degree_i2_budget"] for row in degrees)
    assert all(row["unverified_kernel_probability_upper"] < Fraction(1, 4) for row in batches)
    files = [ROOT/name for name in ("sampler_contract.py", "test_sampler_contract.py", "SAMPLING.md", "verify_sampler.py", "REVIEW_RESOLUTION.md")]
    files += [ROOT.parent/"auxiliary-construction-check-2026-10-26/REVIEW.md",
              ROOT.parent/"auxiliary-construction-check-2026-10-26/exact_controls.py"]
    review = ROOT.parent/"matrix-lift-access-review-2026-10-26/SAMPLER_REVIEW.md"
    if review.exists():
        files.append(review)
    return {"status": "CONDITIONAL_MOD_TWO_SAMPLER_REPLACES_FULL_JACOBIAN_UNIFORMITY",
            "prime_degree_certificates": degrees,
            "relation_batch_bounds": batches,
            "exact_group_order_required": True,
            "group_order_from_native_matrix_implemented": False,
            "native_prime_sampler_implemented": False,
            "quantum_advantage_established": False,
            "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest() for path in files}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = json.loads(json.dumps(report(), default=encode))
    destination = ROOT/"receipt.json"
    if args.write:
        destination.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        if json.loads(destination.read_text()) != result:
            raise SystemExit("FAIL: sampler-contract replay changed")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: 10 prime-degree and101 batch bounds; {len(result['sha256'])} hashes; SHA256 {sha256(destination.read_bytes()).hexdigest()}")
