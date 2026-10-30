"""Replay exact bounds and biased controls; no native curve construction."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from four_list import exact_mixture_moments, overlap_certificate, tower_certificate


ROOT = Path(__file__).resolve().parent


def encode(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)


def report():
    moments = []
    for rank in range(3, 10):
        length = 2**((rank+2)//3)
        alpha = Fraction(1, 4*length)
        atoms = [1, 2, 4, 2**rank-1]
        strengths = [alpha, alpha/2, alpha/3, alpha]
        target = 2**rank-1
        mean, second = exact_mixture_moments(rank, target, atoms, strengths)
        assert mean >= Fraction(7, 8) and second <= Fraction(117, 16)**4
        assert mean**2/second > Fraction(1, 4000)
        moments.append({"rank": rank, "target": target, "atoms": atoms,
                        "strengths": strengths, "mean": mean, "second_moment": second,
                        "success_second_moment_lower": mean**2/second})
    files = [ROOT/name for name in ("four_list.py", "test_four_list.py", "FOUR_LIST.md", "verify_four_list.py", "REVIEW_RESOLUTION.md")]
    files += [ROOT.parent/"auxiliary-construction-check-2026-10-26/REVIEW.md",
              ROOT.parent/"auxiliary-divisor-review-2026-10-26/REVIEW.md"]
    review = ROOT.parent/"auxiliary-four-list-review-2026-10-26/REVIEW.md"
    if review.exists():
        files.append(review)
    return {"status": "CONDITIONAL_CLASSICAL_FOUR_LIST_BOUND_NOT_NATIVE_ALGORITHM",
            "overlap_proof_certificate": overlap_certificate(),
            "tower_degree_checks": [tower_certificate(e) for e in (8, 16, 32, 64, 128)],
            "nonuniform_moment_controls": moments,
            "actual_prime_sampling_implemented": False,
            "actual_auxiliary_divisor_constructed": False,
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
            raise SystemExit("FAIL: four-list replay changed")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: 1296 overlap cases; 7 biased moment controls; {len(result['sha256'])} hashes; SHA256 {sha256(destination.read_bytes()).hexdigest()}")
